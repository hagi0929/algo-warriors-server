from ..model.tag import Tag
from ..model.problem import ProblemDetailed, ProblemMinimal
from ..repos.tag_repos import TagRepos


class TagService:
    @staticmethod
    def get_tag_list(tag_type=None):
        return TagRepos.get_tag_list(tag_type)

    @staticmethod
    def get_tag_by_id(tag_id: int):
        return TagRepos.get_tag_by_id(tag_id)

    @staticmethod
    def create_tag(tag: Tag) -> int:
        return TagRepos.create_tag(tag)

    @staticmethod
    def delete_tag(tag_id: int) -> bool:
        return TagRepos.delete_tag(tag_id)
    
    @staticmethod
    def find_problems_by_tag(tag_type: str, tag_content: str) -> list[ProblemDetailed]:
        return TagRepos.find_problems_by_tag(tag_type, tag_content)
    
    @staticmethod
    def add_tag_to_problem(problem_id: str, tag_id:str):
        TagRepos.add_tag_to_problem(problem_id, tag_id)

    @staticmethod
    def find_problems_with_multiple_tags(difficulty_tags: list[str], subcategory_tags: list[str], source_tags: list[str]) -> list[ProblemDetailed]:
        return TagRepos.find_problems_with_multiple_tags(difficulty_tags, subcategory_tags, source_tags)

    @staticmethod
    def list_all_problems_with_tags() -> list[dict]:
        return TagRepos.list_all_problems_with_tags()
    
    @staticmethod
    def recommend_problems(problem_id) -> list[ProblemMinimal]:
        return TagRepos.recommend_problems(problem_id)

    @staticmethod
    def get_tags_of_problem(problem_id) -> list[Tag]:
        return TagRepos.get_tags_of_problem(problem_id)