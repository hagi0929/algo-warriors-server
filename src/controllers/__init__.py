from flask import Blueprint
from src.controllers.test import test

api = Blueprint('api', __name__)

api.register_blueprint(test, url_prefix="/test")
