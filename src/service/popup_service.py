# Service layer for Popup resources
# Author: Vidhi Ruparel
from ..model.popup import DetailedPopupResource, SimplePopupResource
from ..repos.popup_repos import PopupResourceRepository

class PopupResourceService:
    # Get all resources ordered by stars
    @staticmethod
    def get_all_resources_ordered_by_stars():
        return PopupResourceRepository.get_all_resources_ordered_by_stars()
    
    # Search resources by keyword
    @staticmethod
    def search_resources_by_keyword(keyword):
        return PopupResourceRepository.search_resources_by_keyword(keyword)
    
    # Get popularity data by language
    @staticmethod
    def get_popularity_by_language():
        return PopupResourceRepository.get_popularity_by_language()
        
    # Refresh materialized view
    @staticmethod
    def refresh_materialized_view():
        return PopupResourceRepository.refresh_materialized_view()
    