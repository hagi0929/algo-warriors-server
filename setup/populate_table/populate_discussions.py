

import json
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os


load_dotenv()

def connect_db():
    conn_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    try:
        print("Attempting to connect to the database...")
        connection = psycopg2.connect(**conn_params)
        print("Connection established.")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def execute_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor


def insert_discussion(conn, discussion):
    query = sql.SQL('''
        INSERT INTO Discussion (
            discussion_id, problem_id, parentdiscussion_id, user_id, title, content, created_at, updated_at
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
    ''')
    execute_query(conn, query, (
        discussion['discussion_id'],
        discussion['problem_id'],
        discussion['parentdiscussion_id'],
        discussion['user_id'],
        discussion['title'],
        discussion['content'],
        discussion['created_at'],
        discussion['updated_at']
    ))


def process_json_file(json_file, conn):
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    
    for index, discussion in enumerate(data):
        print(f"Inserting discussion {index + 1}: {discussion['title']}, {discussion['content']}")
        try:
            insert_discussion(conn, discussion)
            print(f"Discussion {index + 1} inserted successfully.")
        except Exception as e:
            print(f"Error inserting discussion {index + 1}: {e}")

    
    conn.commit()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, 'discussions.json')

    connection = connect_db()
    if connection:
        try:
            process_json_file(json_file_path, connection)
        finally:
            connection.close()
            print("Connection closed.")