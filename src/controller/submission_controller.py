from flask import jsonify
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, ValidationError
from werkzeug.exceptions import BadRequest

from src.service.submission_service import SubmissionService

submission_bp = Blueprint("submission", __name__)


class CodeSubmissionSchema(Schema):
    code = fields.Str(required=True)
    problem_id = fields.Int(required=True)
    programming_language = fields.Str(required=True)


class AvailableLanguagesSchema(Schema):
    languages = fields.List(fields.Str(), required=True)


@submission_bp.route('/', methods=['POST'])
@submission_bp.arguments(CodeSubmissionSchema, as_kwargs=True)
def submit_code(**kwargs):
    code = kwargs['code']
    problem_id = kwargs['problem_id']
    programming_language = kwargs['programming_language']

    try:
        result = SubmissionService.submit_code(code, problem_id, programming_language)
        return jsonify(result), 200
    except Exception as e:
        abort(400, description=str(e))


@submission_bp.route('/available_languages', methods=['GET'])
@submission_bp.response(200, AvailableLanguagesSchema)
def get_available_languages():
    try:
        languages = SubmissionService.get_available_languages()
        return {"languages": languages}
    except Exception as e:
        abort(400, description=str(e))
