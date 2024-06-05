from flask import request, Response, json, Blueprint
from werkzeug.exceptions import HTTPException
from flask.views import View

from src.services.test import getHelloWorldService
test = Blueprint("test", __name__)

@test.route('/hello-world', methods = ["GET", "POST"])
def handle_login():
    helloWorldData = getHelloWorldService()
    return Response(
        response=json.dumps({'status': "success", "data": helloWorldData}),
        status=200,
        mimetype='application/json'
    )

@test.errorhandler(HTTPException)
def handle_error(error: HTTPException):
    """ Handle BluePrint JSON Error Response """
    response = {
        'error': error.__class__.__name__,
        'message': error.description,
    }
    return response, error.code