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
    def get_db_conn(self) -> None:
        host=os.environ.get("DB_HOST")
        port=os.environ.get("DB_PORT")
        dbname=os.environ.get("DB_DATABASE_DEV")
        user=os.environ.get("DB_USER")
        password=os.environ.get("DB_PASSWORD")

        connectionParam = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
        return connectionParam

class ProdConfig(Config):
    DEBUG = False
    def get_db_conn(self) -> None:
        host=os.environ.get("DB_HOST")
        port=os.environ.get("DB_PORT")
        dbname=os.environ.get("DB_DATABASE_PROD")
        user=os.environ.get("DB_USER")
        password=os.environ.get("DB_PASSWORD")

        connectionParam = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}'
        return connectionParam
