from flask import Blueprint
from .problem_controller import problem_bp
from .tag_controller import tag_bp
from src.controller.discussion_controller import discussion_bp
from .contest_controller import contest_blueprint
from .popup_controller import popup_resource_blueprint
from werkzeug.exceptions import HTTPException

api = Blueprint('api', __name__)

api.register_blueprint(problem_bp, url_prefix="/problem")
api.register_blueprint(tag_bp, url_prefix="/tag")
api.register_blueprint(discussion_bp, url_prefix='/discussions')
api.register_blueprint(contest_blueprint, url_prefix="/contest")
api.register_blueprint(popup_resource_blueprint, url_prefix="/popup-resources")

@api.errorhandler(HTTPException)
def handle_error(error: HTTPException):
    """ Handle BluePrint JSON Error Response """
    response = {
        'error': error.__class__.__name__,
        'message': error.description,
    }
    return response, error.code
