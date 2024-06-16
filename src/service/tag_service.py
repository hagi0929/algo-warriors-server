from ..model.tag import Tag
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
