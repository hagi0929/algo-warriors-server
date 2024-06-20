from typing import Optional
from ..model.discussion import DiscussionCreationRequest
from ..repos.discussion_repos import DiscussionRepos

class DiscussionService:
    @staticmethod
    def get_discussion_list_by_problem(problem_id: int):
        return DiscussionRepos.get_discussion_list_by_problem_id(problem_id)

    @staticmethod
    def get_discussion_by_id(discussion_id: int):
        return DiscussionRepos.get_discussion_by_id(discussion_id)

    @staticmethod
    def create_discussion(discussion_request: DiscussionCreationRequest) -> int:
        discussion_request.validate()
        new_discussion_id = DiscussionRepos.create_discussion(discussion_request)
        return new_discussion_id

    @staticmethod
    def update_discussion(discussion_id: int, content: str):
        discussion = DiscussionRepos.get_discussion_by_id(discussion_id)
        if not discussion:
            raise ValueError("Discussion not found")
        DiscussionRepos.update_discussion(discussion_id, content)

    @staticmethod
    def delete_discussion(discussion_id: int):
        discussion = DiscussionRepos.get_discussion_by_id(discussion_id)
        if not discussion:
            raise ValueError("Discussion not found")
        DiscussionRepos.delete_discussion(discussion_id)
