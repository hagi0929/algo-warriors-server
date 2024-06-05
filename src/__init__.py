from flask import Flask
import os
from src.config.config import DevConfig
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import event
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

config = DevConfig()


app.config['SQLALCHEMY_DATABASE_URI'] = config.get_db_conn()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from src.controllers import api
app.register_blueprint(api)
