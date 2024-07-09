from flask_smorest import Blueprint
from .problem_controller import problem_bp
from .tag_controller import tag_bp
from .user_controller import user_bp
from src.controller.discussion_controller import discussion_bp
from .contest_controller import contest_blueprint
from .popup_controller import popup_resource_blueprint
from .submission_controller import submission_bp
from werkzeug.exceptions import HTTPException

api_bp = Blueprint('api', __name__)

api_bp.register_blueprint(problem_bp, url_prefix="/problem")
api_bp.register_blueprint(tag_bp, url_prefix="/tag")
api_bp.register_blueprint(discussion_bp, url_prefix='/discussions')
api_bp.register_blueprint(contest_blueprint, url_prefix="/contest")
api.register_blueprint(popup_resource_blueprint, url_prefix="/popup-resources")
api_bp.register_blueprint(user_bp, url_prefix="/user")
api.register_blueprint(submission_bp, url_prefix="/submission")

@api_bp.errorhandler(HTTPException)
def handle_error(error: HTTPException):
    """ Handle BluePrint JSON Error Response """
    response = {
        'error': error.__class__.__name__,
        'message': error.description,
    }
    return response, error.code
