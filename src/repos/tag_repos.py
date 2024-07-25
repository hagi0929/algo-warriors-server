from sqlalchemy.sql import text
from .. import db
from ..model.tag import Tag
from ..model.problem import ProblemDetailed, ProblemMinimal


class TagRepos:
    @staticmethod
    def get_tag_list() -> list[Tag]:
        query = text("""
        SELECT tag_id, type, content FROM Tag
        """)
        result = db.session.execute(query)
        tags = []
        for row in result:
            tags.append(Tag(
                tag_id=row[0],
                type=row[1],
                content=row[2],
            ))
        return tags

    @staticmethod
    def get_tag_by_id(tag_id: int) -> Tag:
        query = text("""
        SELECT tag_id, type, content FROM Tag
        WHERE tag_id = :tid
        """)
        parameters = {'tid': tag_id}
        result = db.session.execute(query, parameters)
        row = result.fetchone()
        if row:
            return Tag(
                tag_id=row[0],
                type=row[1],
                content=row[2],
            )
        return None

    @staticmethod
    def create_tag(tag: Tag) -> int:
        query = text("""
            INSERT INTO Tag (type, content)
            VALUES (:type, :content)
            RETURNING tag_id
        """)
        result = db.session.execute(query, {
            'type': tag.type,
            'content': tag.content,
        })
        tag_id = result.fetchone()[0]

        db.session.commit()
        return tag_id

    @staticmethod
    def delete_tag(tag_id: int) -> bool:
        query = text("""
            DELETE FROM Tag
            WHERE tag_id = :tid
        """)
        result = db.session.execute(query, {'tid': tag_id})
        db.session.commit()
        return result.rowcount > 0

    @staticmethod
    def find_problems_by_tag(tag_type: str, tag_content: str) -> list[ProblemDetailed]:
        query = text("""
        SELECT P.problem_id, P.title, P.description, P.created_by, P.created_at
        FROM Problem P
        JOIN ProblemTag PT ON P.problem_id = PT.problem_id
        JOIN Tag T ON PT.tag_id = T.tag_id
        WHERE T.type = :tag_type AND T.content = :tag_content
        """)
        result = db.session.execute(query, {'tag_type': tag_type, 'tag_content': tag_content})
        problems = [ProblemDetailed(row[0], row[1], row[2], row[3], row[4]) for row in result]
        return problems

    @staticmethod
    def list_all_problems_with_tags() -> list[dict]:
        query = text("""
        SELECT P.problem_id, P.title, T.type, T.content
        FROM Problem P
        JOIN ProblemTag PT ON P.problem_id = PT.problem_id
        JOIN Tag T ON PT.tag_id = T.tag_id
        ORDER BY P.problem_id, T.type
        """)
        result = db.session.execute(query)
        problems_with_tags = []
        for row in result:
            problems_with_tags.append({
                'problem_id': row[0],
                'title': row[1],
                'type': row[2],
                'content': row[3]
            })
        return problems_with_tags

    @staticmethod
    def find_problems_with_multiple_tags(difficulty_tags: list[str], subcategory_tags: list[str],
                                         source_tags: list[str]) -> list[ProblemDetailed]:
        query = text(
            """
        WITH temp AS (
            SELECT P.problem_id, P.title, P.created_by, P.created_at
            FROM Problem P
            JOIN ProblemTag PT ON P.problem_id = PT.problem_id
            JOIN Tag T ON PT.tag_id = T.tag_id
            WHERE T.type = 'difficulty' AND (T.content IN :difficulty_tags OR :difficulty_tags_is_empty = 1)
        ),

        temp2 as (
        SELECT P.problem_id, P.title, P.created_by, P.created_at
        FROM temp P
        JOIN ProblemTag PT ON P.problem_id = PT.problem_id
        JOIN Tag T ON PT.tag_id = T.tag_id
        WHERE T.type = 'subcategory' AND (T.content IN :subcategory_tags OR :subcategory_tags_is_empty = 1)
        )

        SELECT P.problem_id, P.title, P.created_by, P.created_at
        FROM temp2 P
        JOIN ProblemTag PT ON P.problem_id = PT.problem_id
        JOIN Tag T ON PT.tag_id = T.tag_id
        WHERE T.type = 'source' AND (T.content IN :source_tags OR :source_tags_is_empty = 1)
        """)

        difficulty_tags_is_empty = 1 if not difficulty_tags else 0
        subcategory_tags_is_empty = 1 if not subcategory_tags else 0
        source_tags_is_empty = 1 if not source_tags else 0

        result = db.session.execute(query, {
            'difficulty_tags': difficulty_tags,
            'subcategory_tags': subcategory_tags,
            'source_tags': source_tags,
            'difficulty_tags_is_empty': difficulty_tags_is_empty,
            'subcategory_tags_is_empty': subcategory_tags_is_empty,
            'source_tags_is_empty': source_tags_is_empty
        })

        problems = [ProblemDetailed(row[0], row[1], row[2], row[3], row[4]) for row in result]
        return problems

    @staticmethod
    def recommend_problems(problem_id) -> list[ProblemMinimal]:
        query = text("""
SELECT DISTINCT P.problem_id, P.title
FROM Problem P
JOIN ProblemTag PT ON P.problem_id = PT.problem_id
JOIN Tag T ON PT.tag_id = T.tag_id
WHERE P.problem_id != :pid
AND (
    (T.type = 'difficulty' AND T.content NOT IN (
        SELECT T.content
        FROM ProblemTag PT_diff
        JOIN Tag T ON PT_diff.tag_id = T.tag_id
        WHERE PT_diff.problem_id = :pid
        AND T.type = 'difficulty'
    ))
    OR
    (T.type = 'subcategory' AND T.content IN (
        SELECT T.content
        FROM ProblemTag PT_sub
        JOIN Tag T ON PT_sub.tag_id = T.tag_id
        WHERE PT_sub.problem_id = :pid
        AND T.type = 'subcategory'
    ))
)
LIMIT 5;
""")
        result = db.session.execute(query, {'pid': problem_id})
        problems = [ProblemMinimal(row[0], row[1]) for row in result]
        return problems

    @staticmethod
    def add_tag_to_problem(problem_id: str, tag_id: str):
        query = text("""
        INSERT INTO ProblemTag (problem_id, tag_id)
        VALUES (:problem_id, :tag_id)
        """)
        db.session.execute(query, {'problem_id': problem_id, 'tag_id': tag_id})
        db.session.commit()

    @staticmethod
    def get_tags_of_problem(problem_id) -> list[Tag]:
        query = text("""
        SELECT T.tag_id, T.type, T.content
        FROM Tag T
        JOIN ProblemTag PT ON T.tag_id = PT.tag_id
        WHERE PT.problem_id = :pid
        """)
        result = db.session.execute(query, {'pid': problem_id})
        tags = [Tag(row[0], row[1], row[2]) for row in result]
        return tags
