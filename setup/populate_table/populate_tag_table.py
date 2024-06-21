import json
import psycopg2
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')

# Function to connect to PostgreSQL database
def connect_db():
    conn_params = {
        'dbname': '',
        'user': '',
        'password': '',
        'host': '',
        'port': ''
    }
    try:
        print("Attempting to connect to the database...")
        connection = psycopg2.connect(**conn_params)
        print("Connection established.")
        return connection
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

# Function to execute SQL queries and return results
def execute_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor

# Function to insert a new tag or retrieve existing tag_id
def get_or_create_tag(conn, tag_type, content):
    # Check if tag exists
    query = "SELECT tag_id FROM Tag WHERE type = %s AND content = %s"
    result = execute_query(conn, query, (tag_type, content)).fetchone()
    
    if result:
        return result[0]  # Return existing tag_id
    else:
        # Insert new tag and retrieve its id
        query = "INSERT INTO Tag (type, content) VALUES (%s, %s) RETURNING tag_id"
        cursor = execute_query(conn, query, (tag_type, content))
        return cursor.fetchone()[0]

# Main function to process problems.json and populate database
def process_problems_file(json_file, conn):
    # Load JSON data
    with open(json_file, 'r') as f:
        problems = json.load(f)
    
    # Process each problem entry
    for problem in problems:
        problem_id = problem.get('problem_id')
        source = str(problem.get('source'))  # Convert to string
        cf_tags = problem.get('cf_tags')
        difficulty = str(problem.get('difficulty'))  # Convert to string
        
        # Handle source tag
        source_tag_id = get_or_create_tag(conn, "source", source)
        
        # Handle cf_tags
        cf_tag_ids = []
        for cf_tag in cf_tags:
            cf_tag_id = get_or_create_tag(conn, "subcategory", cf_tag)
            cf_tag_ids.append(cf_tag_id)
        
        # Handle difficulty tag
        difficulty_tag_id = get_or_create_tag(conn, "difficulty", difficulty)
        
        # Insert into ProblemTag table
        for cf_tag_id in cf_tag_ids:
            query = "INSERT INTO ProblemTag (problem_id, tag_id) VALUES (%s, %s)"
            execute_query(conn, query, (problem_id, cf_tag_id))
        
        # Insert source and difficulty tags into ProblemTag table
        query = "INSERT INTO ProblemTag (problem_id, tag_id) VALUES (%s, %s)"
        execute_query(conn, query, (problem_id, source_tag_id))
        execute_query(conn, query, (problem_id, difficulty_tag_id))
    
    # Commit changes
    conn.commit()

# Example usage
if __name__ == "__main__":
    problems_json_file = 'setup/populate_table/problems.json'
    
    # Connect to PostgreSQL database
    connection = connect_db()
    if connection:
        try:
            # Process problems.json and populate database
            process_problems_file(problems_json_file, connection)
        finally:
            # Close connection
            connection.close()
            print("Connection closed.")