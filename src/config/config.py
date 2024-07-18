import os


class Config:
    HOST = '0.0.0.0'
    API_TITLE = "AlgoWarriors REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    JWT_SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'false').lower() in ['true', '1']

    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = self.get_db_conn()
        self.REDIS_URL = self.get_redis_conn()

    def get_db_conn(self):
        raise NotImplementedError("Subclasses must implement get_db_conn method")

    def get_redis_conn(self):
        raise NotImplementedError("Subclasses must implement get_db_conn method")


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    PORT = 3000

    def get_db_conn(self):
        host = os.environ["DB_HOST"]
        port = os.environ["DB_PORT"]
        dbname = os.environ["DB_DATABASE"]
        user = os.environ["DB_USER"]
        password = os.environ["DB_PASSWORD"]
        return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'

    def get_redis_conn(self):
        host = os.environ["REDIS_HOST"]
        port = os.environ["REDIS_PORT"]
        password = os.environ["REDIS_PASSWORD"]
        return f'redis://:{password}@{host}:{port}/0'


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    PORT = 5001

    def get_db_conn(self):
        host = os.environ["DB_HOST"]
        port = os.environ["DB_PORT"]
        dbname = os.environ["DB_DATABASE"]
        user = os.environ["DB_USER"]
        password = os.environ["DB_PASSWORD"]
        return f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'

    def get_redis_conn(self):
        host = os.environ["REDIS_HOST"]
        port = os.environ["REDIS_PORT"]
        password = os.environ["REDIS_PASSWORD"]
        return f'redis://:{password}@{host}:{port}/0'


def get_config(env):
    if env == 'dev':
        return DevConfig()
    elif env == 'prod':
        return ProdConfig()
    else:
        raise ValueError(f'{env} is not valid parameter for env')