from typing import List, Optional
from .test_case import TestCase


class AbstractProblem:
    def __init__(self, problem_id: int, title: str, difficulty: int):
        self.problem_id: int = problem_id
        self.title: str = title
        self.difficulty: int = difficulty


class ProblemMinimal(AbstractProblem):
    def __init__(self, problem_id: int, title: str, difficulty: int, tag_ids: List[int] = None):
        super().__init__(problem_id, title, difficulty)
        self.tags: List[int] = tag_ids

    def to_dict(self) -> dict:
        return {
            'problem_id': self.problem_id,
            'title': self.title,
            'difficulty': self.difficulty,
            'tags': self.tags
        }


class ProblemDetailed(AbstractProblem):
    def __init__(self, problem_id: int, title: str, description: str, difficulty: int, created_by: int, created_at: str,
                 tags: Optional[List[str]] = None, test_cases: Optional[List[TestCase]] = None):
        super().__init__(problem_id, title, difficulty)
        self.description: str = description
        self.created_by: int = created_by
        self.created_at: str = created_at
        self.tags: List[int] = tags if tags else []
        self.test_cases: List[TestCase] = test_cases if test_cases else []

    def to_dict(self) -> dict:
        return {
            'problem_id': self.problem_id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'tags': self.tags,
            'test_cases': [tc.to_dict() for tc in self.test_cases]
        }


# still deciding if we need class def for the request
class ProblemCreationRequest(AbstractProblem):
    def __init__(self, title: str, description: str, difficulty: int, created_by: int,
                 tags: Optional[List[int]] = None, test_cases: Optional[dict] = None):
        super().__init__(-1, title, difficulty)
        self.description: str = description
        self.created_by: int = created_by
        self.tags: List[int] = tags if tags else []
        self.test_cases: List[dict] = test_cases if test_cases else []

    def validate(self):
        if not self.title:
            raise ValueError("Title is required")
        if not self.description:
            raise ValueError("Description is required")
        if self.difficulty < 0 or self.difficulty > 5:
            raise ValueError("Difficulty must be between 0 and 5")
        if not isinstance(self.created_by, int):
            raise ValueError("Created by must be an integer")
