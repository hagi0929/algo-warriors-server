

class SimplePopupResource:
    def __init__(self, resource_id: int, resource_name: str, resource_description: str, resource_url: str, homepage: str, stars: int, resource_language: str, topics: str):
        self.resource_id = resource_id
        self.resource_name = resource_name
        self.resource_description = resource_description
        self.resource_url = resource_url
        self.homepage = homepage
        self.stars = stars
        self.resource_language = resource_language
        self.topics = topics
    
    def to_simple_dict(self) -> dict:
        return {
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'resource_description': self.resource_description,
            'resource_url': self.resource_url,
            'homepage': self.homepage,
            'stars': self.stars,
            'resource_language': self.resource_language,
            'topics': self.topics
        }
    
class DetailedPopupResource(SimplePopupResource):
    def __init__(self, resource_id: int, resource_name: str, resource_description: str, resource_url: str, created_at: str, updated_at: str, homepage: str, size: int, stars: int, forks: int, issues: int, watchers: int, resource_language: str, license: str, topics: str, has_issues: bool, has_projects: bool, has_downloads: bool, has_wiki: bool, has_pages: bool, has_discussions: bool, is_fork: bool, is_archived: bool, is_template: bool, default_branch: str):
        super().__init__(resource_id, resource_name, resource_description, resource_url, homepage, stars, resource_language, topics)
        self.created_at = created_at
        self.updated_at = updated_at
        self.size = size
        self.forks = forks
        self.issues = issues
        self.watchers = watchers
        self.license = license
        self.has_issues = has_issues
        self.has_projects = has_projects
        self.has_downloads = has_downloads
        self.has_wiki = has_wiki
        self.has_pages = has_pages
        self.has_discussions = has_discussions
        self.is_fork = is_fork
        self.is_archived = is_archived
        self.is_template = is_template
        self.default_branch = default_branch
    
    def to_dict(self) -> dict:
        base_dict = super().to_simple_dict()
        base_dict.update({
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'size': self.size,
            'forks': self.forks,
            'issues': self.issues,
            'watchers': self.watchers,
            'license': self.license,
            'has_issues': self.has_issues,
            'has_projects': self.has_projects,
            'has_downloads': self.has_downloads,
            'has_wiki': self.has_wiki,
            'has_pages': self.has_pages,
            'has_discussions': self.has_discussions,
            'is_fork': self.is_fork,
            'is_archived': self.is_archived,
            'is_template': self.is_template,
            'default_branch': self.default_branch
        })
        return base_dict
