from werkzeug.exceptions import NotFound

from ..model.problem import ProblemCreationRequest
from ..repos.problem_repos import ProblemRepos


class ProblemService:
    @staticmethod
    def get_problem_list():
        return ProblemRepos.get_problem_list()

    @staticmethod
    def delete_problem(problem_id: int):
        return ProblemRepos.delete_problem_by_id(problem_id)

    @staticmethod
    def get_problem_by_id(problem_id: int):
        obj = ProblemRepos.get_problem_by_id(problem_id)
        if obj is None:
            raise NotFound("Problem not found")
        testcases = ProblemRepos.get_testcases_by_problem_id(problem_id)
        obj.test_cases = testcases
        return obj

    @staticmethod
    def create_problem(problem_request: ProblemCreationRequest) -> int:
        problem_request.validate()
        new_problem_id = ProblemRepos.create_problem(problem_request)
        ProblemRepos.add_test_cases(new_problem_id, problem_request.test_cases)
        return new_problem_id

    @staticmethod
    
    def submit_code(problem_id, code):
        pass

