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


@tag_bp.route('/difficulty/<string:difficulty>', methods=['GET'])
def get_problems_by_difficulty(difficulty):
    problems = TagService.find_problems_by_tag('difficulty', difficulty)
    return jsonify([problem.to_dict() for problem in problems])

@tag_bp.route('/difficulty/<string:difficulty>/subcategory/<string:subcategory>', methods=['GET'])
def get_problems_by_difficulty_and_subcategory(difficulty, subcategory):
    problems = TagService.find_problems_by_tag('difficulty', difficulty)
    problems = [problem for problem in problems if problem.subcategory == subcategory]
    return jsonify([problem.to_dict() for problem in problems])

@tag_bp.route('/multiple', methods=['POST'])
def get_problems_with_multiple_subcategory_tags():
    data = request.get_json()
    difficulty_tags = data.get('difficulty', [])
    subcategory_tags = data.get('subcategory', [])
    source_tags = data.get('source', [])
    problems = TagService.find_problems_with_multiple_tags(difficulty_tags, subcategory_tags, source_tags)
    return jsonify([problem.to_dict() for problem in problems])

@tag_bp.route('/subcategory/<string:subcategory>', methods=['GET'])
def get_problems_by_subcategory(subcategory):
    problems = TagService.find_problems_by_tag('subcategory', subcategory)
    return jsonify([problem.to_dict() for problem in problems])

@tag_bp.route('/source/<string:source>', methods=['GET'])
def get_problems_by_source(source):
    problems = TagService.find_problems_by_tag('source', source)
    return jsonify([problem.to_dict() for problem in problems])

@tag_bp.route('/with_tags', methods=['GET'])
def list_problems_with_tags():
    problems_with_tags = TagService.list_all_problems_with_tags()
    return jsonify(problems_with_tags)

@tag_bp.route('/recommend/<int:problem_id>', methods=['GET'])
def recommend_problems(problem_id):
    problems = TagService.recommend_problems(problem_id)
    return jsonify([problem.to_dict() for problem in problems])