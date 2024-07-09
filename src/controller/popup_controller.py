# Description: Controller for popup resources related operations
# Author: Vidhi Ruparel
from flask import Blueprint, request, jsonify
from src.service.popup_service import PopupResourceService
from src.model.popup import DetailedPopupResource, SimplePopupResource

popup_resource_blueprint = Blueprint('popup_resources', __name__)

# Endpoint to get all resources ordered by stars
@popup_resource_blueprint.route('/', methods=['GET'])
def get_all_resources_ordered_by_stars():
    try:
        resources = PopupResourceService.get_all_resources_ordered_by_stars()
        return jsonify([resource.to_simple_dict() for resource in resources]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Endpoint to search resources by keyword
@popup_resource_blueprint.route('/search', methods=['GET'])
def search_resources_by_keyword():
    keyword = request.args.get('keyword')
    try:
        resources = PopupResourceService.search_resources_by_keyword(keyword)
        return jsonify([resource.to_simple_dict() for resource in resources]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Endpoint to get popularity data by language
@popup_resource_blueprint.route('/popularity-by-language', methods=['GET'])
def get_popularity_by_language():
    try:
        popularity_data = PopupResourceService.get_popularity_by_language()
        return jsonify({'popularity_by_language': popularity_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500    

# Endpoint to refresh materialized view
@popup_resource_blueprint.route('/refresh-view', methods=['POST'])
def refresh_materialized_view():
    try:
        PopupResourceService.refresh_materialized_view()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 500
