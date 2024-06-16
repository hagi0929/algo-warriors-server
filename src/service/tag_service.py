from ..model.tag import Tag
from ..model.problem import ProblemDetailed
from ..repos.tag_repos import TagRepos


class TagService:
    @staticmethod
    def get_tag_list():
        return TagRepos.get_tag_list()

    @staticmethod
    def get_tag_by_id(tag_id: int):
        return TagRepos.get_tag_by_id(tag_id)

    @staticmethod
    def create_tag(tag: Tag) -> int:
        # You might want to add validation here if needed
        return TagRepos.create_tag(tag)

    @staticmethod
    def delete_tag(tag_id: int) -> bool:
        return TagRepos.delete_tag(tag_id)
    
    @staticmethod
    def find_problems_by_tag(tag_type: str, tag_content: str) -> list[ProblemDetailed]:
        return TagRepos.find_problems_by_tag(tag_type, tag_content)

    @staticmethod
    def list_all_problems_with_tags() -> list[dict]:
        return TagRepos.list_all_problems_with_tags()
