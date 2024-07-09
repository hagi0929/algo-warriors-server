from typing import Optional, Dict, List, Union
from sqlalchemy.sql import text
from .. import db
from ..model.user import UserModel, UserSchema


class UserRepos:
    @staticmethod
    def get_user_by_username(username: str) -> UserModel | None:
        query = text("""
        SELECT user_id, username, email, password, role_id FROM serviceuser WHERE username = :username
        """)
        parameters = {'username': username}
        result = db.session.execute(query, parameters)
        row = result.fetchone()
        if row:
            user = UserSchema()
            return user.load(row._mapping)
        return None

    @staticmethod
    def get_user_by_user_id(user_id: int) -> UserModel | None:
        query = text("""
        SELECT user_id, username, email, password, role_id FROM serviceuser WHERE user_id = :user_id
        """)
        parameters = {'user_id': user_id}
        result = db.session.execute(query, parameters)
        row = result.fetchone()
        if row:
            user = UserSchema()
            return user.load(row._mapping)
        return None

    @staticmethod
    def get_permissions_by_role(role_ids: int | List[int] | None = None) -> Dict[int, List[str]]:
        if isinstance(role_ids, int):
            query = text("""
            SELECT role_id, ARRAY_AGG(permission.name) AS permissions
            FROM rolePermission
            LEFT JOIN permission ON rolePermission.permission_id = permission.permission_id
            WHERE role_id = :role_id
            GROUP BY role_id
            """)
            parameters = {'role_id': role_ids}
        elif role_ids:
            query = text("""
            SELECT role_id, ARRAY_AGG(permission.name) AS permissions
            FROM rolePermission
            LEFT JOIN permission ON rolePermission.permission_id = permission.permission_id
            WHERE role_id = ANY(:role_ids)
            GROUP BY role_id
            """)
            parameters = {'role_ids': role_ids}
        else:
            query = text("""
            SELECT role_id, ARRAY_AGG(permission.name) AS permissions
            FROM rolePermission
            LEFT JOIN permission ON rolePermission.permission_id = permission.permission_id
            GROUP BY role_id
            """)
            parameters = {}

        result = db.session.execute(query, parameters)
        rows = result.fetchall()

        permissions_by_role = {row[0]: row[1] for row in rows}
        return permissions_by_role

