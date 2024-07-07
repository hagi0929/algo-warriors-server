from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields

from src.model.problem import ProblemCreationRequest
from src.model.user import LoginRequestSchema
from src.service.user_service import UserService

user_bp = Blueprint("users", __name__)


@user_bp.route("login")
class Login(MethodView):
    @user_bp.arguments(LoginRequestSchema, as_kwargs=True)
    # @user_bp.response(200, TokenResponseSchema)
    def post(self, **kwargs):
        username = kwargs['username']
        password = kwargs['password']
        return UserService.handle_login(username, password)
