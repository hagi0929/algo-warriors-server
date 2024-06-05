from src import db
from sqlalchemy.sql import text
from sqlalchemy import inspect

def test_setup_repos() -> None:
  with db.engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS test (
            ID SERIAL PRIMARY KEY,
            someColumn varchar(255)
        )
    """))
    connection.execute(text("""
        INSERT INTO test (someColumn) VALUES ('hello world')
    """))
    connection.commit()

def list_tables_repos() -> list[str]:
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return tables

def get_test_repos() -> str:
  dd = ""
  with db.engine.connect() as connection:
    result = connection.execute(text("""
      SELECT someColumn FROM test
    """))
    dd =(result.first() or ['didnt work'])[0]
  return dd
  
