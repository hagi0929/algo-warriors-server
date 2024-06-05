from flask import Flask
from src.config.config import DevConfig
from dotenv import load_dotenv
from src.repos import db
load_dotenv()

app = Flask(__name__)

config = DevConfig()


app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_conn()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from .controller.routes import api
app.register_blueprint(api)
