from typing import List

from src import redis_db, db
from .user_repos import UserRepos

class RedisRepos:

    @staticmethod
    def get_role_by_token(token):
        return redis_db.get(f"token:{token}")

    @staticmethod
    def store_token_and_role(token: str, role_id: int):
        redis_db.setex(f"token:{token}", 3600, role_id)

    @staticmethod
    def invalidate_token(token: str):
        redis_db.delete(f"token:{token}")

    @staticmethod
    def get_permissions_by_role(role_id: int):
        permissions = redis_db.get(f"role:{role_id}")
        if permissions:
            return eval(permissions)
        return None

    @staticmethod
    def store_role_permissions(role, permissions):
        redis_db.set(f"role:{role}", str(permissions))
