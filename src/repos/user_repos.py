from typing import Optional, Dict, List
from sqlalchemy.sql import text
from .. import db
from ..model.user import UserModel


class UserRepos:
    @staticmethod
    def get_user_by_username(username: str) -> UserModel | None:
        query = text("""
        SELECT * FROM serviceuser WHERE username = :username
        """)
        parameters = {'username': username}
        result = db.session.execute(query, parameters)
        row = result.fetchone()
        if row.count == 1:
            user = UserModel()
            return user.load(row)
        return None

    @staticmethod
    def get_permissions_by_role(role_id: int) -> List[str]:
        query = text("""
        SELECT name FROM rolePermission
        LEFT JOIN permission ON rolePermission.permission_id = permission.permission_id
        WHERE role_id = :role_id
        """)
        parameters = {'role_id': role_id}
        result = db.session.execute(query, parameters)
        rows = result.fetchall()
        permissions = [row['name'] for row in rows]
        return permissions

