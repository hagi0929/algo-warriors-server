# Description: Controller for popup resources related operations
# Author: Vidhi Ruparel
from flask import Blueprint, request, jsonify
from src.service.popup_service import PopupResourceService
from src.model.popup import DetailedPopupResource, SimplePopupResource

popup_resource_blueprint = Blueprint('popup_resources', __name__)

# Add new popup resource
@popup_resource_blueprint.route('/', methods=['POST'])
def create_popup_resource():
    data = request.json
    resource = DetailedPopupResource(
        resource_id=None,
        resource_name=data['resource_name'],
        resource_description=data['resource_description'],
        resource_url=data['resource_url'],
        homepage=data['homepage'],
        size=data['size'],
        stars=data['stars'],
        forks=data['forks'],
        issues=data['issues']
    )
    created_resource = PopupResourceService.create_popup_resource(resource)
    return jsonify(created_resource.to_dict()), 201

# Get all popup resources
@popup_resource_blueprint.route('/', methods=['GET'])
def get_all_popup_resources():
    resources = PopupResourceService.get_all_popup_resources()
    return jsonify([resource.to_simple_dict() for resource in resources]), 200

# Get popup resource by URL
@popup_resource_blueprint.route('/<string:resource_url>', methods=['GET'])
def get_popup_resource_by_url(resource_url):
    resource = PopupResourceService.get_popup_resource_by_url(resource_url)
    if resource:
        return jsonify(resource.to_dict()), 200
    else:
        return jsonify({'error': 'Resource not found'}), 404

# Update popup resource by URL
@popup_resource_blueprint.route('/<string:resource_url>', methods=['PUT'])
def update_popup_resource_by_url(resource_url):
    data = request.json
    updated_resource = PopupResourceService.update_popup_resource_by_url(resource_url, data)
    if updated_resource:
        return jsonify(updated_resource.to_dict()), 200
    else:
        return jsonify({'error': 'Resource not found'}), 404

# Delete popup resource by URL
@popup_resource_blueprint.route('/<string:resource_url>', methods=['DELETE'])
def delete_popup_resource_by_url(resource_url):
    success = PopupResourceService.delete_popup_resource_by_url(resource_url)
    if success:
        return '', 204
    else:
        return jsonify({'error': 'Resource not found'}), 404
