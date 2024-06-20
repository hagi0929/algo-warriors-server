from flask import Blueprint, jsonify, request
from ..service.discussion_service import DiscussionService
from ..model.discussion import DiscussionCreationRequest

discussion_bp = Blueprint("discussions", __name__)

@discussion_bp.route('/<int:problem_id>', methods=['POST'])

def create_discussion(problem_id):
    data = request.get_json()
    try:
        discussion_request = DiscussionCreationRequest(
            parentdiscussion_id=data['parentdiscussion_id'],
            problem_id=problem_id,
            user_id=data['user_id'],
            content=data['content']
        )
        discussion_id = DiscussionService.create_discussion(discussion_request)
        response = {
            'discussion_id': discussion_id,
            'parentdiscussion_id': discussion_request.parentdiscussion_id,
            'problem_id': discussion_request.problem_id,
            'user_id': discussion_request.user_id,
            'content': discussion_request.content
        }
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@discussion_bp.route('/list/<int:problem_id>', methods=['GET'])
def get_discussion_list(problem_id):
    discussions = [vars(d) for d in DiscussionService.get_discussion_list_by_problem(problem_id)]
    return jsonify(discussions)


@discussion_bp.route('/<int:discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    discussion = DiscussionService.get_discussion_by_id(discussion_id)
    if discussion:
        return jsonify(discussion.to_dict())
    return jsonify({'message': 'Discussion not found'}), 404


@discussion_bp.route('/<int:discussion_id>', methods=['PUT'])
def update_discussion(discussion_id):
    data = request.get_json()
    try:
        content = data['content']
        DiscussionService.update_discussion(discussion_id, content)
        return jsonify({'message': 'Discussion updated successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@discussion_bp.route('/<int:discussion_id>', methods=['DELETE'])
def delete_discussion(discussion_id):
    try:
        DiscussionService.delete_discussion(discussion_id)
        return jsonify({'message': 'Discussion deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
