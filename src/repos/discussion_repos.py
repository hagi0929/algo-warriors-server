from sqlalchemy.sql import text
from .. import db
from ..model.discussion import Discussion, DiscussionCreationRequest
from typing import Optional

class DiscussionRepos:
    @staticmethod
    def get_discussion_list_by_problem_id(problem_id: int) -> list[Discussion]:
        query = text("""
            SELECT discussion_id, 
                parentdiscussion_id, 
                problem_id, 
                user_id, 
                title, 
                content, 
                created_at, 
                updated_at
            FROM Discussion
            WHERE problem_id = :problem_id
        """)
        result = db.session.execute(query, {'problem_id': problem_id})
        discussions = []
        for row in result:
            discussions.append(Discussion(
                discussion_id=row[0],
                parentdiscussion_id=row[1],
                problem_id=row[2],
                user_id=row[3],
                title=row[4],
                content=row[5],
                created_at=row[6],
                updated_at=row[7],
            ))
        return discussions

    @staticmethod
    def get_discussion_by_id(discussion_id: int) -> Discussion:
        query = text("""
            SELECT discussion_id, 
                parentdiscussion_id, 
                problem_id, 
                user_id, 
                title, 
                content, 
                created_at, 
                updated_at
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
                title=row[4],
                content=row[5],
                created_at=row[6],
                updated_at=row[7],
            )
            return discussion
        else:
            return None
        
    @staticmethod
    def get_discussions_by_parent_id(parentdiscussion_id: int) -> list[Discussion]:
        query = text("""
            WITH RECURSIVE subthreads AS (
                SELECT 
                    discussion_id, 
                    parentdiscussion_id, 
                    problem_id, 
                    user_id, 
                    title, 
                    content, 
                    created_at, 
                    updated_at
                FROM 
                    Discussion
                WHERE 
                    discussion_id = :parentdiscussion_id
                UNION ALL
                SELECT 
                    d.discussion_id, 
                    d.parentdiscussion_id, 
                    d.problem_id, 
                    d.user_id, 
                    d.title, 
                    d.content, 
                    d.created_at, 
                    d.updated_at
                FROM 
                    Discussion d
                INNER JOIN 
                    subthreads s 
                ON 
                    d.parentdiscussion_id = s.discussion_id
            )
            SELECT DISTINCT discussion_id, 
                    parentdiscussion_id, 
                    problem_id, 
                    user_id, 
                    title, 
                    content, 
                    created_at, 
                    updated_at
            FROM 
                subthreads
            ORDER BY 
                created_at
        """)
        result = db.session.execute(query, {'parentdiscussion_id': parentdiscussion_id})
        rows = result.fetchall()

        discussions = []
        for row in rows:
            discussion = Discussion(
                discussion_id=row[0],
                parentdiscussion_id=row[1],
                problem_id=row[2],
                user_id=row[3],
                title=row[4],
                content=row[5],
                created_at=row[6],
                updated_at=row[7],
            )
            discussions.append(discussion)
        
        return discussions
    
    @staticmethod
    def create_discussion(discussion_request: DiscussionCreationRequest) -> int:
        query = text("""
            INSERT INTO Discussion (parentdiscussion_id, problem_id, user_id, title, content, created_at, updated_at)
            VALUES (:parentdiscussion_id, :problem_id, :user_id, :title, :content, NOW(), NOW())
            RETURNING discussion_id
        """)
        result = db.session.execute(query, {
            'parentdiscussion_id': discussion_request.parentdiscussion_id,
            'problem_id': discussion_request.problem_id,
            'user_id': discussion_request.user_id,
            'title': discussion_request.title,
            'content': discussion_request.content
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
            UPDATE Discussion
                SET content = 'DELETED COMMENT', updated_at = NOW()
                WHERE discussion_id = :discussion_id
        """)
        db.session.execute(query, {'discussion_id': discussion_id})

        db.session.commit()
