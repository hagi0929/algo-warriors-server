from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from src.repos.redis_repos import RedisRepos


def authorize(required_permissions):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role_id = claims.get('role')
            user_permissions = RedisRepos.get_permissions_by_role(role_id)
            if not all(perm in user_permissions for perm in required_permissions):
                return jsonify(
                    {"error": "Forbidden", "message": "You do not have permission to access this resource"}), 403
            return f(*args, **kwargs)

        return decorated_function

    return decorator


jwt = JWTManager()


def create_middleware(app):
    jwt.init_app(app)

    @app.before_request
    def before_request_func():
        if request.endpoint and 'static' not in request.endpoint:
            try:
                verify_jwt_in_request()
                claims = get_jwt()
                token = request.headers.get('Authorization').split(" ")[1]
                role_id = claims.get('role')

                redis_role_id = RedisRepos.get_role_by_token(token)

                if redis_role_id is None:
                    return jsonify({"error": "Invalid or expired token"}), 401

                if redis_role_id.decode() != str(role_id):
                    RedisRepos.store_token_and_role(token, role_id)
                    redis_role_id = RedisRepos.get_role_by_token(token)

                if redis_role_id.decode() != str(role_id):
                    return jsonify({"error": "Role mismatch"}), 403

            except Exception as e:
                return jsonify({"error": str(e)}), 401

    @app.after_request
    def after_request_func(response):
        return response
