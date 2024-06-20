import psycopg2
import json


def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


def insert_data():
    user_data = read_json_file('users.json')
    problem_data = read_json_file('problems.json')
    test_case_data = read_json_file('test_cases.json')

    db_params = {
        'dbname': '',
        'user': '',
        'password': '',
        'host': '',
        'port': ''
    }

    print("Attempting to connect to the database...")
    connection = psycopg2.connect(**db_params)
    print("Connection established.")
    cursor = connection.cursor()

    user_id = 1
    insert_problem_query = """
    INSERT INTO Problem (problem_id, title, description, difficulty, created_by)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING problem_id
    """
    for problem in problem_data:
        try:
            cursor.execute(insert_problem_query, (
            problem['problem_id'], problem['title'], problem['description'], problem['difficulty'], user_id))
            problem_id = cursor.fetchone()[0]

            # Insert test cases for the problem
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
    # Check data before committing
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
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    insert_data()
