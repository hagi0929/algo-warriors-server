# Description: Controller for contest related operations
# Author: Vidhi Ruparel
from flask import request, jsonify, abort
from src.service.contest_service import ContestService
from src.model.contest import Contest
from flask_smorest import Blueprint

contest_blueprint = Blueprint('contest', __name__)

# Get all contests
@contest_blueprint.route('/contests', methods=['GET'])
def get_all_contests():
    contests = ContestService.get_all_contests()
    return jsonify([contest.to_dict() for contest in contests])

# Get contest by id
@contest_blueprint.route('/contests/<int:contest_id>', methods=['GET'])
def get_contest_by_id(contest_id):
    contest = ContestService.get_contest_by_id(contest_id)
    if contest is None:
        abort(404, description="Contest not found")
    return jsonify(contest.to_dict())

# Create contest
@contest_blueprint.route('/contests', methods=['POST'])
def create_contest():
    data = request.json
    contest = Contest(
        title=data['title'],
        description=data['description'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        created_by=data['created_by']
    )
    created_contest = ContestService.create_contest(contest)
    return jsonify(created_contest.to_dict()), 201

# Delete contest by id
@contest_blueprint.route('/contests/<int:contest_id>', methods=['DELETE'])
def delete_contest(contest_id):
    contest = ContestService.get_contest_by_id(contest_id)
    if contest is None:
        abort(404, description="Contest not found")
    ContestService.delete_contest(contest_id)
    return '', 204

# Register user to contest
@contest_blueprint.route('/contests/<int:contest_id>/register', methods=['POST'])
def register_user_to_contest(contest_id):
    data = request.json
    user_id = data['user_id']
    ContestService.register_user_to_contest(contest_id, user_id)
    return '', 204

# Add problem to contest
@contest_blueprint.route('/contests/<int:contest_id>/add-problem', methods=['POST'])
def add_problem_to_contest(contest_id):
    data = request.json
    problem_id = data['problem_id']
    ContestService.add_problem_to_contest(contest_id, problem_id)
    return '', 204

# Get contest problems
@contest_blueprint.route('/contests/<int:contest_id>/problems', methods=['GET'])
def get_contest_problems(contest_id):
    problems = ContestService.get_contest_problems(contest_id)
    return jsonify([problem.to_dict() for problem in problems])

# Get contest participants
@contest_blueprint.route('/contests/<int:contest_id>/participants', methods=['GET'])
def get_contest_participants(contest_id):
    participants = ContestService.get_contest_participants(contest_id)
    return jsonify(participants)

# Get contests the user is participating in
@contest_blueprint.route('/contests/participants/<int:user_id>', methods=['GET'])
def get_contests_participating(user_id):
    contests = ContestService.get_contests_participating(user_id)
    return jsonify([contest.to_dict() for contest in contests])

# Submit contest problem
@contest_blueprint.route('/contests/<int:contest_id>/submit', methods=['POST'])
def submit_contest_problem():
    data = request.json
    participant_id = data['participant_id']
    problem_id = data['problem_id']
    submission = data['submission']
    submission_id = ContestService.submit_contest_problem(participant_id, problem_id, submission)
    return jsonify({'submission_id': submission_id}), 201

# Get contest within a time range
@contest_blueprint.route('/contests/date-range', methods=['GET'])
def get_contests_within_date_range():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    contests = ContestService.get_contests_within_date_range(start_date, end_date)
    return jsonify([c.to_dict() for c in contests])

# Get contest participants ranked
@contest_blueprint.route('/contests/<int:contest_id>/participants/ranked', methods=['GET'])
def get_contest_participants_ranked(contest_id):
    n = int(request.args.get('n', 3))  # Default to top 3 if not provided
    participants = ContestService.get_contest_participants_ranked(contest_id, n)
    return jsonify(participants)

# Get user's score and rank in contest
@contest_blueprint.route('/contests/<int:contest_id>/users/<int:user_id>/rank', methods=['GET'])
def get_user_score_and_rank(contest_id, user_id):
    user_score_and_rank = ContestService.get_user_score_and_rank(contest_id, user_id)
    if user_score_and_rank:
        return jsonify(user_score_and_rank)
    else:
        return jsonify({'message': 'User not found or has no submissions in this contest'}), 404

# Declare winner of contest
@contest_blueprint.route('/contests/<int:contest_id>/declare_winner', methods=['POST'])
def declare_winner(contest_id):
    try:
        ContestService.declare_winner(contest_id)
        return jsonify({'message': 'Winner declared successfully'}), 200
    except ValueError as e:
        return jsonify({'message': str(e)}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
