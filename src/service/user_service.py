from flask_jwt_extended import create_access_token

from ..model.tag import Tag
from ..model.problem import ProblemDetailed
from ..repos.redis_repos import RedisRepos
from ..repos.user_repos import UserRepos
from ..utils.auth import check_password


class UserService:
    @staticmethod
    def handle_login(username: str, password: str) -> str:
        user = UserRepos.get_user_by_username(username)
        if user is None or not check_password(password, user.password):
            raise Exception()
        role_id = user.role_id
        permissions = RedisRepos.get_permissions_by_role(role_id)
        additional_claims = {"role": role_id}
        token = create_access_token(identity=user.user_id, additional_claims=additional_claims)
        RedisRepos.store_token_and_role(token, role_id)
        return token
