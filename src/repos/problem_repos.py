from sqlalchemy.sql import text
from .. import db
from ..model.problem import ProblemMinimal, ProblemDetailed, ProblemCreationRequest, ProblemDashboard
from ..model.test_case import TestCase


class ProblemRepos:
    @staticmethod
    def get_problem_list() -> list[ProblemMinimal]:
        query = text("""
        SELECT problem_id, title FROM Problem ORDER BY problem_id LIMIT 200
        """)
        result = db.session.execute(query)
        problems = []
        for row in result:
            problems.append(ProblemMinimal(
                problem_id=row[0],
                title=row[1]
            ))

        return problems

    # (SELECT DISTINCT problem_id FROM ProblemTag WHERE pt.tag_id in:tags)
    # p
    @staticmethod
    def get_problem_dashboard_list(filters: dict, pagination=None) -> list[ProblemDashboard]:
        if pagination is None:
            pagination = {}
        select_query = """
            p.problem_id, p.title,
                   array_agg(t.tag_id) FILTER (WHERE t.type = 'subcategory') as tags,
                   MAX(t.tag_id) FILTER (WHERE t.type = 'difficulty') as difficulty
        """
        from_query = """
            Problem p
            NATURAL LEFT JOIN ProblemTag pt
            NATURAL LEFT JOIN Tag t
        """
        where_query = []
        group_query = "p.problem_id, p.title"
        order_query = ""
        parameters = {}
        if 'title' in filters:
            where_query.append("p.title ILIKE :title")
            parameters["title"] = f"%{filters['title']}%"

        if 'categories' in filters:
            from_query = """
            (SELECT DISTINCT problem_id FROM ProblemTag WHERE tag_id IN :categories) as ptemp
            NATURAL LEFT JOIN Problem p
            NATURAL LEFT JOIN ProblemTag pt
            NATURAL LEFT JOIN Tag t
            """
            parameters["categories"] = tuple(filters['categories'])

        if 'contest_id' in filters:
            from_query += " NATURAL JOIN ContestProblem c"
            where_query.append("c.contest_id = :contest_id")
            parameters["contest_id"] = filters['contest_id']

        if 'difficulty' in filters:
            group_query += " HAVING MAX(t.tag_id) FILTER (WHERE t.type = 'difficulty') IN :difficulty"
            parameters["difficulty"] = tuple(filters['difficulty'])

        if 'sort_by' in filters:
            column = filters['sort_by']
            if column in ["problem_id", "title", "difficulty"]:
                order_query = f"ORDER BY {column}"

        parameters["limit"] = pagination.get('page_size', 10)
        parameters["offset"] = (pagination.get('page_index', 1) - 1) * pagination.get('page_size', 10)

        raw_where_query = ""
        if len(where_query) > 0:
            raw_where_query += " WHERE " + " , ".join(where_query) + " "
        query = f"""
        SELECT {select_query} 
        FROM {from_query} 
        {raw_where_query} 
        GROUP BY {group_query} 
        {order_query} 
        LIMIT :limit OFFSET :offset
        """

        result = db.session.execute(text(query), parameters)
        problems = []
        for row in result:
            problems.append(ProblemDashboard(
                problem_id=row[0],
                title=row[1],
                categories=row[2],
                difficulty=row[3]
            ))

        return problems

    @staticmethod
    def get_problem_by_id(problem_id: int) -> ProblemDetailed | None:
        query = text("""
        SELECT problem_id, title, description, created_by, created_at FROM Problem p
            NATURAL LEFT JOIN serviceuser u
            WHERE problem_id = :pid
        """)
        parameters = {'pid': problem_id}
        result = db.session.execute(query, parameters)
        row = result.first()
        if row is None:
            return None
        problem = ProblemDetailed(
            problem_id=row[0],
            title=row[1],
            description=row[2],
            created_by=row[3],
            created_at=row[4],
        )
        return problem

    @staticmethod
    def get_testcases_by_problem_id(problem_id: int, include_private: bool = False) -> list[TestCase]:
        query = text("""
        SELECT testcase_id, problem_id, input, output, is_public FROM TestCase p
            WHERE problem_id = :pid
            AND (:include_private = TRUE OR is_public = TRUE)
        """)
        parameters = {'pid': problem_id, 'include_private': include_private}
        result = db.session.execute(query, parameters)
        test_cases = [TestCase(row[0], row[1], row[2], row[3], row[4]) for row in result]
        return test_cases

    @staticmethod
    def create_problem(problem_request: ProblemCreationRequest) -> int:
        query = text("""
            INSERT INTO problem (title, description, created_by)
            VALUES (:title, :description, :created_by)
            RETURNING problem_id
        """)
        result = db.session.execute(query, {
            'title': problem_request.title,
            'description': problem_request.description,
            'created_by': problem_request.created_by
        })
        problem_id = result.fetchone()[0]

        db.session.commit()
        return problem_id

    @staticmethod
    def delete_problem_by_id(problem_id: int) -> bool:
        query = text("""
            DELETE FROM problem WHERE problem_id = :problem_id
        """)
        result = db.session.execute(query, {'problem_id': problem_id})
        db.session.commit()

        if result.rowcount == 0:
            return False
        return True

    @staticmethod
    def add_test_cases(problem_id: int, test_cases: list[dict]) -> None:
        query = text("""
            INSERT INTO testcase (problem_id, input, output, is_public)
            VALUES (:problem_id, :input, :output, :is_public)
        """)
        for test_case in test_cases:
            db.session.execute(query, {
                'problem_id': problem_id,
                'input': test_case['input'],
                'output': test_case['output'],
                'is_public': test_case.get('is_public', True)
            })
        db.session.commit()
