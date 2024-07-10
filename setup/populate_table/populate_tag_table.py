import json
import psycopg2
from dotenv import dotenv_values




def connect_db():
    conn_params = {
        'dbname': 'cs348proj',
        'user': 'cs348',
        'password': 'cs348',
        'host': '132.145.98.138',
        'port': '5432'
    }
    print("Attempting to connect to the database...")
    connection = psycopg2.connect(**conn_params)
    print("Connection established.")
    return connection

def execute_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor


def get_or_create_tag(conn, tag_type, content):
    
    query = "SELECT tag_id FROM Tag WHERE type = %s AND content = %s"
    result = execute_query(conn, query, (tag_type, content)).fetchone()
    
    if result:
        return result[0]  
    else:
        
        query = "INSERT INTO Tag (type, content) VALUES (%s, %s) RETURNING tag_id"
        cursor = execute_query(conn, query, (tag_type, content))
        return cursor.fetchone()[0]


def process_problems_file(json_file, conn):
    
    with open(json_file, 'r') as f:
        problems = json.load(f)
    
    
    for problem in problems:
        problem_id = problem.get('problem_id')
        source = str(problem.get('source'))  
        cf_tags = problem.get('cf_tags')
        difficulty = str(problem.get('difficulty'))  
        
        
        source_tag_id = get_or_create_tag(conn, "source", source)
        
        
        cf_tag_ids = []
        for cf_tag in cf_tags:
            cf_tag_id = get_or_create_tag(conn, "subcategory", cf_tag)
            cf_tag_ids.append(cf_tag_id)
        
        
        difficulty_tag_id = get_or_create_tag(conn, "difficulty", difficulty)
        
        
        for cf_tag_id in cf_tag_ids:
            query = "INSERT INTO ProblemTag (problem_id, tag_id) VALUES (%s, %s)"
            execute_query(conn, query, (problem_id, cf_tag_id))
        
        
        query = "INSERT INTO ProblemTag (problem_id, tag_id) VALUES (%s, %s)"
        execute_query(conn, query, (problem_id, source_tag_id))
        execute_query(conn, query, (problem_id, difficulty_tag_id))
    
    
    conn.commit()


if __name__ == "__main__":
    problems_json_file = 'problems.json'
    
    
    connection = connect_db()
    if connection:
        try:
            
            process_problems_file(problems_json_file, connection)
        finally:
            
            connection.close()
            print("Connection closed.")