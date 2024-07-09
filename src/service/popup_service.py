# Service layer for Popup resources
# Author: Vidhi Ruparel
from ..model.popup import DetailedPopupResource, SimplePopupResource
from ..repos.popup_repos import PopupResourceRepository

class PopupResourceService:
    # Create popup resource
    @staticmethod
    def create_popup_resource(resource: DetailedPopupResource) -> DetailedPopupResource:
        return PopupResourceRepository.create_popup_resource(resource)
    
    # Get all popup resources
    @staticmethod
    def get_all_popup_resources() -> list:
        return PopupResourceRepository.get_all_popup_resources()
    
    # Get popup resource by URL
    @staticmethod
    def get_popup_resource_by_url(resource_url: str) -> SimplePopupResource:
        return PopupResourceRepository.get_popup_resource_by_url(resource_url)
    
    # Update popup resource by URL
    @staticmethod
    def update_popup_resource_by_url(resource_url: str, data: dict) -> DetailedPopupResource:
        return PopupResourceRepository.update_popup_resource_by_url(resource_url, data)
    
    # Delete popup resource by URL
    @staticmethod
    def delete_popup_resource_by_url(resource_url: str) -> bool:
        return PopupResourceRepository.delete_popup_resource_by_url(resource_url)
