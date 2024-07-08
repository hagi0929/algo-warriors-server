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
    res = SubmissionService.submit_code(code, problem_id, programming_language)
    return res
