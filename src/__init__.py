from flask import Flask
from src.config.config import DevConfig
from dotenv import load_dotenv
from src.repos import db
from flask_jwt_extended import JWTManager
import redis


load_dotenv()

app = Flask(__name__)

config = DevConfig()

app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_conn()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "some-random-thing"

jwt = JWTManager(app)

db.init_app(app)
redis_db = redis.Redis.from_url(config.get_redis_conn())

from .controller.routes import api

app.register_blueprint(api)

from .middleware.middleware import create_middleware
create_middleware(app)
