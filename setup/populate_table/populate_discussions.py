# Description: Python script to populate the Discussion table in the database with data from a JSON file.
# Author: Vidhi Ruparel
import json
import psycopg2
from psycopg2 import sql
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')

# Function to connect to PostgreSQL database
def connect_db():
    conn_params = {
        'dbname': 'cs348proj',
        'user': 'cs348',
        'password': 'cs348',
        'host': '132.145.98.138',
        'port': '5432'
    }
    try:
        print("Attempting to connect to the database...")
        connection = psycopg2.connect(**conn_params)
        print("Connection established.")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to execute SQL queries
def execute_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor

# Function to insert data into Discussion table
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

# Main function to process the JSON file and populate the database
def process_json_file(json_file, conn):
    # Read JSON data
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Process each discussion
    for index, discussion in enumerate(data):
        print(f"Inserting discussion {index + 1}: {discussion['title']}, {discussion['content']}")
        try:
            insert_discussion(conn, discussion)
            print(f"Discussion {index + 1} inserted successfully.")
        except Exception as e:
            print(f"Error inserting discussion {index + 1}: {e}")

    # Commit changes
    conn.commit()

# Execute the script
if __name__ == "__main__":
    json_file_path = 'discussions.json'
    
    # Connect to PostgreSQL database
    connection = connect_db()
    if connection:
        try:
            # Process JSON file and populate database
            process_json_file(json_file_path, connection)
        finally:
            # Close connection
            connection.close()
            print("Connection closed.")