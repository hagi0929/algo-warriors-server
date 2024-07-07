from functools import wraps
from typing import List

from flask import request, jsonify
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt, get_jwt_identity
from src.repos.redis_repos import RedisRepos
from src.repos.user_repos import UserRepos
from src import jwt


def require_auth(required_permissions: None | List[str] = None, pass_auth_info: bool = False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            token = request.headers.get('Authorization').split(" ")[1]
            user_id: int = get_jwt_identity()
            user_role_id = RedisRepos.get_role_by_token(token)

            if user_role_id is None:
                user_data = UserRepos.get_user_by_user_id(user_id)
                if not user_data:
                    return jsonify({"error": "User not found"}), 403
                user_role_id = user_data.role_id
                RedisRepos.store_token_and_role(token, user_role_id)

            user_permissions = RedisRepos.get_permissions_by_role(user_role_id)
            user_role_id = int(user_role_id)
            if user_permissions is None:
                user_permissions = UserRepos.get_permissions_by_role(user_role_id)[user_role_id]
                RedisRepos.store_role_permissions(user_role_id, user_permissions)

            if required_permissions is not None and len(required_permissions) > 0:
                if not all(perm in user_permissions for perm in required_permissions):
                    return jsonify(
                        {"error": "Forbidden", "message": "You do not have permission to access this resource"}
                    ), 403
                if pass_auth_info:
                    kwargs["auth_data"] = {
                        "permissions": user_permissions
                    }
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def create_middleware(app):
    jwt.init_app(app)

    @app.before_request
    def before_request_func():
        pass

    @app.after_request
    def after_request_func(response):
        return response
