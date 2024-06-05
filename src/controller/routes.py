from flask import Blueprint
from .test_controller import test

api = Blueprint('api', __name__)

api.register_blueprint(test, url_prefix="/test")
