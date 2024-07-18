from flask_jwt_extended import create_access_token
from werkzeug.exceptions import Unauthorized, Conflict

from ..repos.redis_repos import RedisRepos
from ..repos.user_repos import UserRepos
from ..utils.auth import check_password, hash_password


class UserService:
    @staticmethod
    def handle_login(username: str, password: str) -> str:
        user = UserRepos.get_user_by_username(username)
        if user is None or not check_password(password, user.password):
            raise Unauthorized("Username not found or incorrect password")
        role_id = user.role_id
        additional_claims = {"role": role_id}
        token = create_access_token(identity=user.user_id, additional_claims=additional_claims)
        RedisRepos.store_token_and_role(token, role_id)
        return token

    @staticmethod
    def handle_logout(jwt: str):
        RedisRepos.blacklist_jwt(jwt, "LOGOUT")

    @staticmethod
    def register_user(email: str, username: str, password: str):
        hashed_password = hash_password(password)
        res = UserRepos.register_user(email, username, hashed_password)
        if res is not None:
            raise Conflict(f'{res} is used')