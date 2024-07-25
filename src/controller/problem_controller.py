from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from flask_smorest import Blueprint
from marshmallow import Schema, post_load, fields
from werkzeug import Response
from werkzeug.exceptions import NotFound

from src.middleware.middleware import require_auth
from src.model.problem import ProblemCreationRequest
from src.service.problem_service import ProblemService

problem_bp = Blueprint("problems", __name__)


class TestCaseSchema(Schema):
    input = fields.Str(required=True)
    output = fields.Str(required=True)


class CreateProblemSchema(Schema):
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    tags = fields.Int(many=True, required=False)
    test_cases = fields.List(fields.Nested(TestCaseSchema, required=False))

    @post_load
    def convert(self, data, **kwargs):
        return ProblemCreationRequest(**data)


class ProblemSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    tags = fields.List(fields.Int())
    test_cases = fields.List(fields.Nested(TestCaseSchema))
    created_by = fields.Int()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


@problem_bp.route('/', methods=['POST'])
@problem_bp.arguments(CreateProblemSchema, as_kwargs=True)
@problem_bp.response(201)
@require_auth()
def create_problem(**kwargs):
    try:
        user_id = get_jwt_identity()
        problem_request = ProblemCreationRequest(
            title=kwargs['title'],
            description=kwargs['description'],
            created_by=user_id,
            tags=kwargs.get('tags', []),
            test_cases=kwargs.get('test_cases', [])
        )
        problem_id = ProblemService.create_problem(problem_request)
        response = {
            'problem_id': problem_id,
        }
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


class ProblemMinimalSchema(Schema):
    problem_id = fields.Int()
    title = fields.Str()
    difficulty = fields.Str()


@problem_bp.route('/list', methods=['GET'])
@problem_bp.response(200, ProblemMinimalSchema(many=True))
def get_problem_list():
    problems = [vars(p) for p in ProblemService.get_problem_list()]
    return jsonify(problems)


class ProblemDashboardSchema(Schema):
    problem_id = fields.Int()
    title = fields.Str()
    difficulty = fields.Int()
    categories = fields.Int(many=True)


class ProblemFilterSchema(Schema):
    title = fields.String(required=False)
    difficulty = fields.String(required=False)
    categories = fields.String(required=False)
    contest_id = fields.String(required=False)
    sort_by = fields.String(required=False)


class PagenationSchema(Schema):
    page_index = fields.Int()
    page_size = fields.Int()


@problem_bp.route('/dashboard-list', methods=['GET'])
@problem_bp.response(200, ProblemDashboardSchema(many=True))
@problem_bp.arguments(PagenationSchema, location="query", as_kwargs=True)
@problem_bp.arguments(ProblemFilterSchema, location="query", as_kwargs=True)
def get_problem_dashboard_list(**kwargs):
    filter_options = {}
    if "categories" in kwargs and kwargs["categories"]:
        filter_options["categories"] = kwargs["categories"].split(',')
    if "difficulty" in kwargs and kwargs["difficulty"]:
        filter_options["difficulty"] = kwargs["difficulty"].split(',')
    if "title" in kwargs and kwargs["title"]:
        filter_options["title"] = kwargs["title"]
    if "contest_id" in kwargs and kwargs["contest_id"]:
        filter_options["contest_id"] = kwargs["contest_id"]
    if "sort_by" in kwargs and kwargs["sort_by"]:
        filter_options["sort_by"] = kwargs["sort_by"]

    pagination = {
        'page_size': request.args.get('page_size', 10, type=int),
        'page_index': request.args.get('page_index', 1, type=int)
    }
    problems = [vars(p) for p in ProblemService.get_problem_dashboard_list(filter_options, pagination)]
    return jsonify(problems)


@problem_bp.route('/<int:problem_id>', methods=['GET'])
@problem_bp.response(200, ProblemSchema)
@problem_bp.doc(responses={404: "Problem not found"})
# @require_auth([])
def get_problem(problem_id):
    problem = ProblemService.get_problem_by_id(problem_id)
    if problem is None:
        raise NotFound("Problem not found")
    return jsonify(problem.to_dict())


@problem_bp.route('/<int:problem_id>', methods=['DELETE'])
@require_auth([], pass_auth_info=True)
@problem_bp.response(204)
@problem_bp.doc(responses={404: "Problem not found"})
def delete_problem(problem_id, **kwargs):
    auth_info = kwargs['auth_data']
    user_id = auth_info.get('user_id', None)
    list_of_permissions = auth_info.get('permissions', [])
    problem = ProblemService.get_problem_by_id(problem_id)
    if problem is None:
        raise NotFound("Problem not found")
    if "delete_all_problem" in list_of_permissions or (
            "delete_own_problem" in list_of_permissions and user_id == problem.problem_id):
        ProblemService.delete_problem(problem_id)
    return Response(problem.to_dict())
