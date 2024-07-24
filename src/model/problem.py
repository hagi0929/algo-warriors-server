from typing import List, Optional
from .test_case import TestCase


class AbstractProblem:
    def __init__(self, problem_id: int, title: str):
        self.problem_id: int = problem_id
        self.title: str = title


class ProblemMinimal(AbstractProblem):
    def __init__(self, problem_id: int, title: str, description:str):
        super().__init__(problem_id, title)
        self.description: str = description
        

    def to_dict(self) -> dict:
        return {
            'problem_id': self.problem_id,
            'title': self.title,
            'description': self.description
        }


class ProblemDetailed(AbstractProblem):
    def __init__(self, problem_id: int, title: str, description: str, created_by: int, created_at: str,
                 tags: Optional[List[str]] = None, test_cases: Optional[List[TestCase]] = None):
        super().__init__(problem_id, title)
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
            'created_by': self.created_by,
            'created_at': self.created_at,
            'tags': self.tags,
            'test_cases': [tc.to_dict() for tc in self.test_cases]
        }


class ProblemCreationRequest(AbstractProblem):
    def __init__(self, title: str, description: str, created_by: int,
                 tags: Optional[List[int]] = None, test_cases: List[dict] = None):
        super().__init__(-1, title)
        self.description: str = description
        self.created_by: int = created_by
        self.tags: List[int] = tags if tags else []
        self.test_cases: List[dict] = test_cases if test_cases else []

    def validate(self):
        if not self.title:
            raise ValueError("Title is required")
        if not self.description:
            raise ValueError("Description is required")
        if not isinstance(self.created_by, int):
            raise ValueError("Created by must be an integer")
