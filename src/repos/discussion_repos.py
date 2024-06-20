from sqlalchemy.sql import text
from .. import db
from ..model.discussion import Discussion
from typing import Optional

class DiscussionRepos:
    @staticmethod
    def get_discussion_list_by_problem_id(problem_id: int) -> list[Discussion]:
        query = text("""
            SELECT discussion_id, parentdiscussion_id, problem_id, user_id, content, created_at, updated_at
            FROM Discussion
            WHERE problem_id = :problem_id
        """)
        parameters = {'problem_id': problem_id}
        result = db.session.execute(query, parameters)
        discussions = []
        for row in result:
            discussions.append(Discussion(
                discussion_id=row[0],
                parentdiscussion_id=row[1],
                problem_id=row[2],
                user_id=row[3],
                content=row[4],
                created_at=row[5],
                updated_at=row[6],
            ))
        return discussions

    @staticmethod
    def get_discussion_by_id(discussion_id: int) -> Discussion:
        query = text("""
            SELECT discussion_id, parentdiscussion_id, problem_id, user_id, content, created_at, updated_at
            FROM Discussion
            WHERE discussion_id = :discussion_id
        """)
        parameters = {'discussion_id': discussion_id}
        result = db.session.execute(query, parameters)
        row = result.first()
        if row:
            discussion = Discussion(
                discussion_id=row[0],
                parentdiscussion_id=row[1],
                problem_id=row[2],
                user_id=row[3],
                content=row[4],
                created_at=row[5],
                updated_at=row[6]
            )
            return discussion
        else:
            return None

    @staticmethod
    def create_discussion(parentdiscussion_id: Optional[int], problem_id: int, user_id: int, content: str) -> int:
        query = text("""
            INSERT INTO Discussion (parentdiscussion_id, problem_id, user_id, content, created_at, updated_at)
            VALUES (:parentdiscussion_id, :problem_id, :user_id, :content, NOW(), NOW())
            RETURNING discussion_id
        """)
        result = db.session.execute(query, {
            'parentdiscussion_id': parentdiscussion_id,
            'problem_id': problem_id,
            'user_id': user_id,
            'content': content
        })
        discussion_id = result.fetchone()[0]
        db.session.commit()
        return discussion_id


    @staticmethod
    def update_discussion(discussion_id: int, content: str) -> None:
        query = text("""
            UPDATE Discussion
            SET content = :content, updated_at = NOW()
            WHERE discussion_id = :discussion_id
        """)
        db.session.execute(query, {
            'content': content,
            'discussion_id': discussion_id
        })
        db.session.commit()

    @staticmethod
    def delete_discussion(discussion_id: int) -> None:
        query = text("""
            DELETE FROM Discussion
            WHERE discussion_id = :discussion_id
        """)
        db.session.execute(query, {'discussion_id': discussion_id})
        db.session.commit()