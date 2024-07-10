from ..repos.popup_repos import PopupResourceRepository


class PopupResourceService:

    @staticmethod
    def get_all_resources_ordered_by_stars():
        return PopupResourceRepository.get_all_resources_ordered_by_stars()

    @staticmethod
    def search_resources_by_keyword(keyword):
        return PopupResourceRepository.search_resources_by_keyword(keyword)

    @staticmethod
    def get_popularity_by_language():
        return PopupResourceRepository.get_popularity_by_language()

    @staticmethod
    def refresh_materialized_view():
        return PopupResourceRepository.refresh_materialized_view()
