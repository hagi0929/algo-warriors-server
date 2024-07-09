# Description: Model for Popup Resource
# Author: Vidhi Ruparel
class SimplePopupResource:
    def __init__(self, resource_id: int, resource_name: str, resource_description: str, resource_url: str, homepage: str):
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.resource_description = resource_description
        self.resource_url = resource_url
        self.homepage = homepage
    
    def to_simple_dict(self) -> dict:
        return {
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'resource_description': self.resource_description,
            'resource_url': self.resource_url,
            'homepage': self.homepage
        }
    
class DetailedPopupResource(SimplePopupResource):
    def __init__(self, resource_id: int, resource_name: str, resource_description: str, resource_url: str, homepage: str, size: int, stars: int, forks: int, issues: int):
        super().__init__(resource_id, resource_name, resource_description, resource_url, homepage)
        self.size = size
        self.stars = stars
        self.forks = forks
        self.issues = issues
    
    def to_dict(self) -> dict:
        base_dict = super().to_simple_dict()
        base_dict.update({
            'size': self.size,
            'stars': self.stars,
            'forks': self.forks,
            'issues': self.issues
        })
        return base_dict
