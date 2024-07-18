from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields
from werkzeug.exceptions import NotFound, BadRequest

from src.model.tag import Tag
from src.service.tag_service import TagService

tag_bp = Blueprint("tags", __name__)


class TagSchema(Schema):
    tag_id = fields.Int(required=True)
    type = fields.Str(required=True)
    content = fields.Str(required=True)


class TagCreateSchema(Schema):
    type = fields.Str(required=True)
    content = fields.Str(required=True)


class TagResponseSchema(Schema):
    tag_id = fields.Int()
    type = fields.Str()
    content = fields.Str()


class ProblemTagSchema(Schema):
    problem_id = fields.Int(required=True)
    tag_id = fields.Int(required=True)


class ProblemsByTagsSchema(Schema):
    difficulty = fields.List(fields.Str(), required=False)
    subcategory = fields.List(fields.Str(), required=False)
    source = fields.List(fields.Str(), required=False)


# Routes

@tag_bp.route('/', methods=['POST'])
@tag_bp.arguments(TagCreateSchema)
@tag_bp.response(201, TagResponseSchema)
def create_tag(data):
    try:
        tag = Tag(
            type=data['type'],
            content=data['content']
        )
        tag_id = TagService.create_tag(tag)
        response = {
            'tag_id': tag_id,
            'type': tag.type,
            'content': tag.content
        }
        return response
    except ValueError as e:
        abort(400, description=str(e))


@tag_bp.route('/list', methods=['GET'])
@tag_bp.response(200, TagResponseSchema(many=True))
def get_tag_list():
    tags = TagService.get_tag_list()
    return tags


@tag_bp.route('/<int:tag_id>', methods=['GET'])
@tag_bp.response(200, TagResponseSchema)
def get_tag(tag_id):
    tag = TagService.get_tag_by_id(tag_id)
    if tag:
        return tag
    abort(404, description='Tag not found')


@tag_bp.route('/<int:tag_id>', methods=['DELETE'])
@tag_bp.response(200, {"message": fields.Str()})
def delete_tag(tag_id):
    success = TagService.delete_tag(tag_id)
    if success:
        return {'message': 'Tag deleted successfully'}
    abort(404, description='Tag not found')


@tag_bp.route('/difficulty/<string:difficulty>', methods=['GET'])
@tag_bp.response(200, TagResponseSchema(many=True))
def get_problems_by_difficulty(difficulty):
    problems = TagService.find_problems_by_tag('difficulty', difficulty)
    return problems


@tag_bp.route('/add_tag_to_problem', methods=['POST'])
@tag_bp.arguments(ProblemTagSchema)
@tag_bp.response(200, {"message": fields.Str()})
def add_tag_to_problem(data):
    problem_id = data['problem_id']
    tag_id = data['tag_id']
    TagService.add_tag_to_problem(problem_id, tag_id)
    return {'message': 'Tag added to problem'}


@tag_bp.route('/multiple', methods=['POST'])
@tag_bp.arguments(ProblemsByTagsSchema)
@tag_bp.response(200, TagResponseSchema(many=True))
def get_problems_with_multiple_subcategory_tags(data):
    difficulty_tags = data.get('difficulty', [])
    subcategory_tags = data.get('subcategory', [])
    source_tags = data.get('source', [])
    problems = TagService.find_problems_with_multiple_tags(difficulty_tags, subcategory_tags, source_tags)
    return problems


@tag_bp.route('/subcategory/<string:subcategory>', methods=['GET'])
@tag_bp.response(200, TagResponseSchema(many=True))
def get_problems_by_subcategory(subcategory):
    problems = TagService.find_problems_by_tag('subcategory', subcategory)
    return problems


@tag_bp.route('/source/<string:source>', methods=['GET'])
@tag_bp.response(200, TagResponseSchema(many=True))
def get_problems_by_source(source):
    problems = TagService.find_problems_by_tag('source', source)
    return problems


@tag_bp.route('/recommend/<int:problem_id>', methods=['GET'])
@tag_bp.response(200, TagResponseSchema(many=True))
def recommend_problems(problem_id):
    problems = TagService.recommend_problems(problem_id)
    return problems


@tag_bp.route('/<int:problem_id>/tags', methods=['GET'])
@tag_bp.response(200, TagResponseSchema(many=True))
def get_tags_of_problem(problem_id):
    tags = TagService.get_tags_of_problem(problem_id)
    return tags
