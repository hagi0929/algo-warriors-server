from flask import Blueprint, jsonify, request
import http.client
import ssl
import certifi

from src.service.submission_service import SubmissionService

submission_bp = Blueprint("submission", __name__)

@submission_bp.route('/', methods=['POST'])
def submit_code():
    code = request.json.get('code')
    problem_id = request.json.get('problem_id')
    programming_language = request.json.get('programming_language')
    return SubmissionService.submit_code(code, problem_id, programming_language)

@submission_bp.route('/available_languages', methods=['GET'])
def get_available_languages():
    return SubmissionService.get_available_languages()