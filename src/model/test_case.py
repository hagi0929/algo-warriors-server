class TestCase:
    def __init__(self, test_case_id: int, problem_id: int, input: str, output: str, is_public: bool = True):
        self.test_case_id = test_case_id
        self.problem_id = problem_id
        self.input = input
        self.output = output
        self.is_public = is_public

    def to_dict(self) -> dict:
        return {
            'test_case_id': self.test_case_id,
            'problem_id': self.problem_id,
            'input': self.input,
            'output': self.output,
            'is_public': self.is_public
        }
