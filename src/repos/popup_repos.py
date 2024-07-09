# Repository for Popup Resource model
# Author: Vidhi Ruparel
from sqlalchemy.sql import text
from .. import db
from ..model.popup import DetailedPopupResource, SimplePopupResource

class PopupResourceRepository:
    # Refresh materialized view
    @staticmethod
    def refresh_materialized_view():
        query = text("REFRESH MATERIALIZED VIEW PopupResourcesView")
        db.session.execute(query)
        db.session.commit()
    
    # Create popup resource
    @staticmethod
    def create_popup_resource(resource: DetailedPopupResource) -> DetailedPopupResource:
        query = text("""
            INSERT INTO PopupResource (resource_name, resource_description, resource_url, homepage, size, stars, forks, issues)
            VALUES (:resource_name, :resource_description, :resource_url, :homepage, :size, :stars, :forks, :issues)
            RETURNING resource_id
        """)
        result = db.session.execute(query, {
            'resource_name': resource.resource_name,
            'resource_description': resource.resource_description,
            'resource_url': resource.resource_url,
            'homepage': resource.homepage,
            'size': resource.size,
            'stars': resource.stars,
            'forks': resource.forks,
            'issues': resource.issues
        })
        resource_id = result.fetchone()[0]
        db.session.commit()
        PopupResourceRepository.refresh_materialized_view()
        resource.resource_id = resource_id
        return resource
    
    # Get all popup resources
    @staticmethod
    def get_all_popup_resources() -> list:
        query = text("SELECT * FROM PopupResourcesView")
        result = db.session.execute(query)
        rows = result.fetchall()
        resources = [SimplePopupResource(
            resource_id=row['resource_id'],
            resource_name=row['resource_name'],
            resource_description=row['resource_description'],
            resource_url=row['resource_url'],
            homepage=row['homepage']
        ) for row in rows]
        return resources
    
    # Get popup resource by URL
    @staticmethod
    def get_popup_resource_by_url(resource_url: str) -> SimplePopupResource:
        query = text("SELECT * FROM PopupResourcesView WHERE resource_url = :resource_url")
        result = db.session.execute(query, {'resource_url': resource_url})
        row = result.fetchone()
        if row:
            return SimplePopupResource(
                resource_id=row['resource_id'],
                resource_name=row['resource_name'],
                resource_description=row['resource_description'],
                resource_url=row['resource_url'],
                homepage=row['homepage']
            )
        return None
    
    # Update popup resource by URL
    @staticmethod
    def update_popup_resource_by_url(resource_url: str, data: dict) -> DetailedPopupResource:
        query = text("""
            UPDATE PopupResource
            SET resource_name = :resource_name,
                resource_description = :resource_description,
                resource_url = :resource_url,
                homepage = :homepage,
                size = :size,
                stars = :stars,
                forks = :forks,
                issues = :issues
            WHERE resource_url = :original_resource_url
            RETURNING resource_id, resource_name, resource_description, resource_url, homepage, size, stars, forks, issues
        """)
        result = db.session.execute(query, {
            'resource_name': data.get('resource_name'),
            'resource_description': data.get('resource_description'),
            'resource_url': data.get('resource_url'),
            'homepage': data.get('homepage'),
            'size': data.get('size'),
            'stars': data.get('stars'),
            'forks': data.get('forks'),
            'issues': data.get('issues'),
            'original_resource_url': resource_url
        })
        db.session.commit()
        PopupResourceRepository.refresh_materialized_view()
        row = result.fetchone()
        if row:
            return DetailedPopupResource(
                resource_id=row['resource_id'],
                resource_name=row['resource_name'],
                resource_description=row['resource_description'],
                resource_url=row['resource_url'],
                homepage=row['homepage'],
                size=row['size'],
                stars=row['stars'],
                forks=row['forks'],
                issues=row['issues']
            )
        return None
    
    # Delete popup resource by URL
    @staticmethod
    def delete_popup_resource_by_url(resource_url: str) -> bool:
        query = text("DELETE FROM PopupResource WHERE resource_url = :resource_url")
        result = db.session.execute(query, {'resource_url': resource_url})
        db.session.commit()
        PopupResourceRepository.refresh_materialized_view()
        return result.rowcount > 0
