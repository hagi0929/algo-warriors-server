import psycopg2
import json
from dotenv import load_dotenv
import os


load_dotenv()

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def insert_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    user_data = read_json_file(os.path.join(script_dir, 'users.json'))
    problem_data = read_json_file(os.path.join(script_dir, 'problems.json'))
    test_case_data = read_json_file(os.path.join(script_dir, 'test_cases.json'))
    discussions_data = read_json_file(os.path.join(script_dir, 'discussions.json'))

    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }

    print("Attempting to connect to the database...")
    connection = psycopg2.connect(**db_params)
    print("Connection established.")
    cursor = connection.cursor()

    user_id = 1
    insert_problem_query = """
    INSERT INTO Problem (problem_id, title, description, created_by)
    VALUES (%s, %s, %s, %s)
    RETURNING problem_id
    """
    for problem in problem_data:
        try:
            cursor.execute(insert_problem_query, (
            problem['problem_id'], problem['title'], problem['description'], user_id))
            problem_id = cursor.fetchone()[0]

            
            insert_test_case_query = """
            INSERT INTO TestCase (problem_id, is_public, input, output)
            VALUES (%s, %s, %s, %s)
            """
            for test_case in test_case_data:
                if test_case['problem_id'] == problem_id:
                    cursor.execute(insert_test_case_query,
                                   (problem_id, test_case['is_public'], test_case['input'], test_case['output']))
        except psycopg2.errors.UniqueViolation:
            connection = psycopg2.connect(**db_params)
            cursor = connection.cursor()
            continue

    
    insert_discussion_query = """
    INSERT INTO Discussion (problem_id, parentdiscussion_id, user_id, title, content, created_at, updated_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    for discussion in discussions_data:
        try:
            cursor.execute(insert_discussion_query, (
                discussion['problem_id'], discussion['parentdiscussion_id'], discussion['user_id'],
                discussion['title'], discussion['content'], discussion['created_at'], discussion['updated_at']))
            connection.commit()  
        except psycopg2.errors.UniqueViolation:
            connection.rollback()
            continue
        except psycopg2.Error as e:
            print(f"An error occurred: {e}")
            connection.rollback()
            continue

    
    cursor.execute("SELECT * FROM ServiceUser")
    service_user_rows = cursor.fetchall()
    print("\nServiceUser Table:")
    for row in service_user_rows:
        print(row)

    cursor.execute("SELECT * FROM Problem")
    problem_rows = cursor.fetchall()
    print("\nProblem Table:")
    for row in problem_rows:
        print(row)

    cursor.execute("SELECT * FROM TestCase")
    test_case_rows = cursor.fetchall()
    print("\nTestCase Table:")
    for row in test_case_rows:
        print(row)

    cursor.execute("SELECT * FROM Discussion")
    discussion_rows = cursor.fetchall()
    print("\nDiscussion Table:")
    for row in discussion_rows:
        print(row)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_data()
