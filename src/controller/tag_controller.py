from flask import Blueprint, jsonify, request

from src.model.tag import Tag
from src.service.tag_service import TagService

tag_bp = Blueprint("tags", __name__)


@tag_bp.route('/', methods=['POST'])
def create_tag():
    data = request.get_json()
    try:
        tag = Tag(
            tag_id=data['tag_id'],
            type=data['type'],
            content=data['content']
        )
        tag_id = TagService.create_tag(tag)
        response = {
            'tag_id': tag_id,
            'type': tag.type,
            'content': tag.content
        }
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@tag_bp.route('/list', methods=['GET'])
def get_tag_list():
    tags = [tag.to_dict() for tag in TagService.get_tag_list()]
    return jsonify(tags)


@tag_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = TagService.get_tag_by_id(tag_id)
    if tag:
        return jsonify(tag.to_dict())
    return jsonify({'message': 'Tag not found'}), 404


@tag_bp.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    success = TagService.delete_tag(tag_id)
    if success:
        return jsonify({'message': 'Tag deleted successfully'}), 200
    return jsonify({'message': 'Tag not found'}), 404

@tag_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Cool'}), 200
