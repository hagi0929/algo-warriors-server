import os
import psycopg2


class Config:
    HOST = '0.0.0.0'
    PORT = 80

    def get_db_conn(self) -> None:
        raise NotImplementedError()


class DevConfig(Config):
    ENV = "development"
    PORT = 3000
    DEBUG = True

    def get_db_conn(self) -> str:
        host = os.environ.get("DB_HOST")
        port = os.environ.get("DB_PORT")
        dbname = os.environ.get("DB_DATABASE")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")

        connection_param = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
        return connection_param

    def get_redis_conn(self) -> str:
        host = os.environ.get("REDIS_HOST")
        port = os.environ.get("REDIS_PORT")
        password = os.environ.get("REDIS_PASSWORD")

        connection_param = f'redis://:{password}@{host}:{port}/0'

        return connection_param


class ProdConfig(Config):
    DEBUG = False

    def get_db_conn(self) -> str:
        host = os.environ.get("DB_HOST")
        port = os.environ.get("DB_PORT")
        dbname = os.environ.get("DB_DATABASE")
        user = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")

        connection_param = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
        return connection_param

    def get_redis_conn(self) -> str:
        host = os.environ.get("REDIS_HOST")
        port = os.environ.get("REDIS_PORT")
        password = os.environ.get("REDIS_PASSWORD")

        connection_param = f'redis://:{password}@{host}:{port}/0'

        return connection_param
