from flask import request, jsonify, abort
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, ValidationError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

from src.service.contest_service import ContestService

contest_blueprint = Blueprint('contest', __name__)


class ContestSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    description = fields.Str()


class ContestCreateSchema(Schema):
    name = fields.Str(required=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    description = fields.Str(required=True)


class UserRegistrationSchema(Schema):
    user_id = fields.Int(required=True)


class ProblemAddSchema(Schema):
    problem_id = fields.Int(required=True)


class SubmissionSchema(Schema):
    participant_id = fields.Int(required=True)
    problem_id = fields.Int(required=True)
    submission = fields.Str(required=True)


class RankSchema(Schema):
    n = fields.Int(required=False, missing=3)


# Error Handlers

@contest_blueprint.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({"error": str(e)}), 404


@contest_blueprint.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": str(e)}), 400


@contest_blueprint.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    return jsonify({"error": str(e)}), 500


@contest_blueprint.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({"error": e.messages}), 400


# Routes

@contest_blueprint.route('/contests', methods=['GET'])
@contest_blueprint.response(200, ContestSchema(many=True))
def get_all_contests():
    contests = ContestService.get_all_contests()
    return contests


@contest_blueprint.route('/contests/<int:contest_id>', methods=['GET'])
@contest_blueprint.response(200, ContestSchema)
def get_contest_by_id(contest_id):
    contest = ContestService.get_contest_by_id(contest_id)
    if contest is None:
        abort(404, description="Contest not found")
    return contest


@contest_blueprint.route('/contests', methods=['POST'])
@contest_blueprint.arguments(ContestCreateSchema)
@contest_blueprint.response(201, ContestSchema)
def create_contest(data):
    created_contest = ContestService.create_contest(data)
    return created_contest


@contest_blueprint.route('/contests/<int:contest_id>', methods=['DELETE'])
def delete_contest(contest_id):
    contest = ContestService.get_contest_by_id(contest_id)
    if contest is None:
        abort(404, description="Contest not found")
    ContestService.delete_contest(contest_id)
    return '', 204


@contest_blueprint.route('/contests/<int:contest_id>/register', methods=['POST'])
@contest_blueprint.arguments(UserRegistrationSchema)
def register_user_to_contest(data, contest_id):
    user_id = data['user_id']
    ContestService.register_user_to_contest(contest_id, user_id)
    return '', 204


@contest_blueprint.route('/contests/<int:contest_id>/add-problem', methods=['POST'])
@contest_blueprint.arguments(ProblemAddSchema)
def add_problem_to_contest(data, contest_id):
    problem_id = data['problem_id']
    ContestService.add_problem_to_contest(contest_id, problem_id)
    return '', 204


@contest_blueprint.route('/contests/<int:contest_id>/problems', methods=['GET'])
def get_contest_problems(contest_id):
    problems = ContestService.get_contest_problems(contest_id)
    return jsonify(problems)


@contest_blueprint.route('/contests/<int:contest_id>/participants', methods=['GET'])
def get_contest_participants(contest_id):
    participants = ContestService.get_contest_participants(contest_id)
    return jsonify(participants)


@contest_blueprint.route('/contests/participants/<int:user_id>', methods=['GET'])
@contest_blueprint.response(200, ContestSchema(many=True))
def get_contests_participating(user_id):
    contests = ContestService.get_contests_participating(user_id)
    return contests


@contest_blueprint.route('/contests/<int:contest_id>/submit', methods=['POST'])
@contest_blueprint.arguments(SubmissionSchema)
def submit_contest_problem(data, contest_id):
    participant_id = data['participant_id']
    problem_id = data['problem_id']
    submission = data['submission']
    submission_id = ContestService.submit_contest_problem(participant_id, problem_id, submission)
    return jsonify({'submission_id': submission_id}), 201


@contest_blueprint.route('/contests/date-range', methods=['GET'])
@contest_blueprint.response(200, ContestSchema(many=True))
def get_contests_within_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    contests = ContestService.get_contests_within_date_range(start_date, end_date)
    return contests


@contest_blueprint.route('/contests/<int:contest_id>/participants/ranked', methods=['GET'])
@contest_blueprint.arguments(RankSchema, location="query")
def get_contest_participants_ranked(query_args, contest_id):
    n = query_args['n']
    participants = ContestService.get_contest_participants_ranked(contest_id, n)
    return jsonify(participants)


@contest_blueprint.route('/contests/<int:contest_id>/users/<int:user_id>/rank', methods=['GET'])
def get_user_score_and_rank(contest_id, user_id):
    user_score_and_rank = ContestService.get_user_score_and_rank(contest_id, user_id)
    if user_score_and_rank:
        return jsonify(user_score_and_rank)
    else:
        abort(404, description='User not found or has no submissions in this contest')


@contest_blueprint.route('/contests/<int:contest_id>/declare_winner', methods=['POST'])
def declare_winner(contest_id):
    try:
        ContestService.declare_winner(contest_id)
        return jsonify({'message': 'Winner declared successfully'}), 200
    except ValueError as e:
        abort(404, description=str(e))
    except Exception as e:
        abort(500, description=str(e))
