from flask import jsonify, request
from flask_smorest import Blueprint
from src.middleware.middleware import require_auth
from src.model.problem import ProblemCreationRequest
from src.service.problem_service import ProblemService

problem_bp = Blueprint("problems", __name__)


@problem_bp.route('/', methods=['POST'])
def create_problem():
    data = request.get_json()
    try:
        problem_request = ProblemCreationRequest(
            title=data['title'],
            description=data['description'],
            created_by=data['created_by'],
            tags=data.get('tags', []),
            test_cases=data.get('test_cases', [])
        )
        problem_id = ProblemService.create_problem(problem_request)
        response = {
            'problem_id': problem_id,
            'title': problem_request.title,
            'description': problem_request.description,
            'created_by': problem_request.created_by,
            'tags': problem_request.tags,
            'test_cases': problem_request.test_cases
        }
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@problem_bp.route('/list', methods=['GET'])
def get_problem_list():
    problems = [vars(p) for p in ProblemService.get_problem_list()]
    return jsonify(problems)


@problem_bp.route('/<int:problem_id>', methods=['GET'])
@require_auth([])
def get_problem(problem_id):
    problem = ProblemService.get_problem_by_id(problem_id)
    if problem:
        return jsonify(problem.to_dict())
    return jsonify({'message': 'Problem not found'}), 404


@problem_bp.route('/<int:problem_id>/submit', methods=['POST'])
@require_auth(required_permissions=["submit_code"], pass_auth_info=True)
def submit_code(problem_id):
    code = request.json.get('code')  
    result = ProblemService.submit_code(problem_id, code)
    return jsonify(result)
