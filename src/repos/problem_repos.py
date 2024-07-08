from sqlalchemy.sql import text
from .. import db
from ..model.problem import ProblemMinimal, ProblemDetailed, ProblemCreationRequest
from ..model.test_case import TestCase


class ProblemRepos:
    @staticmethod
    def get_problem_list() -> list[ProblemMinimal]:
        query = text("""
        SELECT problem_id, title FROM Problem
        """)
        result = db.session.execute(query)
        problems = []
        for row in result:
            problems.append(ProblemMinimal(
                problem_id=row[0],
                title=row[1],
            ))

        # TODO add tags
        # query = text("""
        # SELECT problem_id, title, difficulty FROM Problem
        # """)
        return problems

    @staticmethod
    def get_problem_by_id(problem_id: int) -> ProblemDetailed:
        query = text("""
        SELECT problem_id, title, description, created_by, created_at FROM Problem p
            NATURAL LEFT JOIN serviceuser u
            WHERE problem_id = :pid
        """)
        parameters = {'pid': problem_id}
        result = db.session.execute(query, parameters)
        row = result.first()
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
            NATURAL LEFT JOIN serviceuser u
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
