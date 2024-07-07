from flask_jwt_extended import create_access_token

from ..model.tag import Tag
from ..model.problem import ProblemDetailed
from ..repos.redis_repos import RedisRepos
from ..repos.user_repos import UserRepos
from ..utils.auth import check_pwd


class UserService:
    @staticmethod
    def handle_login(username: str, password: str) -> str:
        user = UserRepos.get_user_by_username(username)
        if user is None or not check_pwd(password, user.password):
            raise Exception()
        role_id = user.role_id
        permissions = RedisRepos.get_permissions_by_role(role_id)
        additional_claims = {"role": role_id}
        token = create_access_token(identity=user.username, additional_claims=additional_claims)
        RedisRepos.store_token_and_role(token, role_id)
        return token
