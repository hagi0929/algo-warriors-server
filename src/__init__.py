from flask import Flask
from src.config.config import get_config
from src.repos import db, redis_db
from .controller import api
from .controller.routes import api_bp
from .middleware.middleware import create_middleware
from flask_cors import CORS


def create_app(config_name):
    app = Flask(__name__)

    config = get_config(config_name)
    app.config.from_object(config)

    db.init_app(app)
    redis_db.init_app(app)
    api.init_app(app)
    api.register_blueprint(api_bp)
    CORS(app)  # TODO find elegant way to manage cors

    create_middleware(app)

    return app
