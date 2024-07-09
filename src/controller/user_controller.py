from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint
from src.middleware.middleware import require_auth

from src.model.user import LoginRequestSchema
from src.service.user_service import UserService

user_bp = Blueprint("users", __name__)


@user_bp.route("/login")
class Login(MethodView):
    @user_bp.arguments(LoginRequestSchema, as_kwargs=True)
    def post(self, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        return UserService.handle_login(username, password)


@user_bp.route('/logout', methods=['GET'])
@require_auth(pass_auth_info=True)
def user_logout(**kwargs):
    user_id: int = get_jwt_identity()
    return ""
