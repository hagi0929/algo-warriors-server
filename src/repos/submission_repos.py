from sqlalchemy.sql import text
from .. import db


class SubmissionRepos:
    @staticmethod
    def get_input_output(problem_id: int):
        query = text("""
        SELECT testcase_id, input, output FROM TestCase
        WHERE problem_id = :pid
        """)
        parameters = {'pid': problem_id}
        result = db.session.execute(query, parameters)
        raw_results = result.fetchall()
        results = []
        for row in raw_results:
            results.append({
                'testcase_id': row[0],
                'input': row[1],
                'output': row[2]
            })
        return results
