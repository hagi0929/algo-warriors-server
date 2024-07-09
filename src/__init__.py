from flask import Flask
from src.config.config import DevConfig
from dotenv import load_dotenv
from src.repos import db
from flask_jwt_extended import JWTManager
import redis
from flask_smorest import Api


load_dotenv()

app = Flask(__name__)

config = DevConfig()

app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_conn()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "some-random-thing"
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "AlgoWarriors REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

jwt = JWTManager(app)

db.init_app(app)
redis_db = redis.Redis.from_url(config.get_redis_conn())

from .controller.routes import api_bp
api = Api(app)
api.register_blueprint(api_bp)

from .middleware.middleware import create_middleware
create_middleware(app)
