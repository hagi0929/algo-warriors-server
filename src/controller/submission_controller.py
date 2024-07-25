from flask import request
from flask_smorest import Blueprint

from src.service.submission_service import SubmissionService

submission_bp = Blueprint("submission", __name__)


@submission_bp.route('/', methods=['POST'])
def submit_code():
    code = request.json.get('code')
    problem_id = request.json.get('problem_id')
    programming_language = request.json.get('programming_language')
    print(code)
    return SubmissionService.submit_code(code, problem_id, programming_language)
    #return [{"message": "Code submitted successfully"}], 200


@submission_bp.route('/available_languages', methods=['GET'])
def get_available_languages():
    return SubmissionService.get_available_languages()
