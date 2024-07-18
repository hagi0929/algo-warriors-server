from typing import Optional, Dict, List, Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from .. import db
from ..model.user import UserModel, UserSchema


class UserRepos:
    @staticmethod
    def register_user(email: str, username: str, password: str, role_id=1) -> list | None:
        redundant_columns = []

        insert_query = text("""
        INSERT INTO serviceuser (email, username, password, role_id) VALUES (:email, :username, :password, :role_id)
        """)
        check_email_query = text("SELECT 1 FROM serviceuser WHERE email = :email")
        check_username_query = text("SELECT 1 FROM serviceuser WHERE username = :username")
        reset_sequence_query = text(
            "SELECT setval('serviceuser_user_id_seq', (SELECT MAX(user_id) FROM serviceuser) + 1)")

        parameters = {
            'email': email,
            'username': username,
            'password': password,
            'role_id': role_id
        }

        def insert_user():
            db.session.execute(insert_query, parameters)
            db.session.commit()

        try:
            insert_user()
            return None
        except IntegrityError as e:
            db.session.rollback()
            email_exists = db.session.execute(check_email_query, {'email': email}).scalar()
            if email_exists:
                redundant_columns.append('email')
            username_exists = db.session.execute(check_username_query, {'username': username}).scalar()
            if username_exists:
                redundant_columns.append('username')

            if not redundant_columns:
                db.session.execute(reset_sequence_query)
                db.session.commit()
                return UserRepos.register_user(email, username, password, role_id)

        return redundant_columns

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
