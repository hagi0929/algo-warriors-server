# Repository for Popup Resource model
# Author: Vidhi Ruparel
from sqlalchemy.sql import text
from .. import db
from ..model.popup import DetailedPopupResource, SimplePopupResource

class PopupResourceRepository:
    # Get all resources ordered by stars
    @staticmethod
    def get_all_resources_ordered_by_stars():
        query = text('''
            SELECT *
            FROM PopupResourcesView
            ORDER BY stars DESC;
        ''')
        result = db.session.execute(query)
        return [SimplePopupResource(
            resource_id=row[0],
            resource_name=row[1],
            resource_description=row[2],
            resource_url=row[3],
            homepage=row[4],
            stars=row[5],
            resource_language=row[6],
            topics=row[7]
        ) for row in result]
    
    # Search resources by keyword
    @staticmethod
    def search_resources_by_keyword(keyword):
        query = text('''
            SELECT *
            FROM PopupResourcesView
            WHERE resource_name ILIKE :keyword
               OR topics ILIKE :keyword
            ORDER BY stars DESC;
        ''')
        processed_keyword = keyword.replace(' ', '-')
        result = db.session.execute(query, {'keyword': f'%{processed_keyword}%'})
        return [SimplePopupResource(
            resource_id=row[0],
            resource_name=row[1],
            resource_description=row[2],
            resource_url=row[3],
            homepage=row[4],
            stars=row[5],
            resource_language=row[6],
            topics=row[7]
        ) for row in result]
    
    # Get popularity data by language
    @staticmethod
    def get_popularity_by_language():
        query = text('''
            SELECT resource_language AS language,
                   AVG(stars) AS avg_stars,
                   COUNT(*) AS resource_count
            FROM PopupResourcesView
            WHERE resource_language IS NOT NULL
            GROUP BY resource_language
            ORDER BY avg_stars DESC;
        ''')
        result = db.session.execute(query)
        popularity_data = []
        for row in result:
            popularity_data.append({
                'language': row[0],
                'avg_stars': row[1],
                'resource_count': row[2]
            })
        return popularity_data
    
    # Refresh materialized view
    @staticmethod
    def refresh_materialized_view():
        query = text("REFRESH MATERIALIZED VIEW PopupResourcesView")
        db.session.execute(query)
        db.session.commit()
    