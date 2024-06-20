from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Discussion:
    def __init__(self, discussion_id, parentdiscussion_id, problem_id, user_id, content, created_at, updated_at):
        self.discussion_id = discussion_id
        self.parentdiscussion_id = parentdiscussion_id
        self.problem_id = problem_id
        self.user_id = user_id
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at


    def to_dict(self) -> dict:
        return {
            'discussion_id': self.discussion_id,
            'problem_id': self.problem_id,
            'parentdiscussion_id': self.parentdiscussion_id,
            'user_id': self.user_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
    
    def update_content(self, new_content: str):
        self.content = new_content
        self.updated_at = datetime.now()

class DiscussionCreationRequest:
    def __init__(self, parentdiscussion_id: Optional[int], problem_id: int, user_id: int, content: str):
        self.problem_id: int = problem_id
        self.parentdiscussion_id: Optional[int] = parentdiscussion_id
        self.user_id: int = user_id
        self.content: str = content

    def validate(self):
        if not isinstance(self.problem_id, int):
            raise ValueError("Problem ID must be an integer")
        if not isinstance(self.parentdiscussion_id, (int, type(None))):
            raise ValueError("Parent discussion ID must be an integer or None")
        if not isinstance(self.user_id, int):
            raise ValueError("User ID must be an integer")
        if not self.content or not isinstance(self.content, str):
            raise ValueError("Content is required and must be a string")
        if len(self.content) > 500:
            raise ValueError("Content must not exceed 500 characters")
