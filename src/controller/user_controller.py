from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_smorest import Blueprint
from src.middleware.middleware import require_auth

from src.model.user import LoginRequestSchema, RegisterRequestSchema
from src.service.user_service import UserService

user_bp = Blueprint("users", __name__)


@user_bp.route("/login", methods=['POST'])
@user_bp.arguments(LoginRequestSchema, as_kwargs=True)
def user_login(**kwargs):
    username = kwargs['username']
    password = kwargs['password']
    return UserService.handle_login(username, password)


@user_bp.route('/logout', methods=['DELETE'])
@require_auth([])
def user_logout(**kwargs):
    jti = get_jwt()["jti"]
    UserService.handle_logout(jti)
    return "success"


@user_bp.route("/register", methods=['POST'])
@user_bp.arguments(RegisterRequestSchema, as_kwargs=True)
def user_login(**kwargs):
    email = kwargs['email']
    username = kwargs['username']
    password = kwargs['password']
    UserService.register_user(email, username, password)
    return UserService.handle_login(username, password)
