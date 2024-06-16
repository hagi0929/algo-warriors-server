from flask import Blueprint
from .problem_controller import problem_bp
from .tag_controller import tag_bp
from werkzeug.exceptions import HTTPException

api = Blueprint('api', __name__)

api.register_blueprint(problem_bp, url_prefix="/problem")
api.register_blueprint(tag_bp, url_prefix="/tag")

@api.errorhandler(HTTPException)
def handle_error(error: HTTPException):
    """ Handle BluePrint JSON Error Response """
    response = {
        'error': error.__class__.__name__,
        'message': error.description,
    }
    return response, error.code
