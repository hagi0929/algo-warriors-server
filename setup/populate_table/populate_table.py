import psycopg2
import json


# Function to read JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)


# Function to insert data into the database
def insert_data():
    # Read data from JSON files
    user_data = read_json_file('users.json')
    problem_data = read_json_file('problems.json')
    test_case_data = read_json_file('test_cases.json')

    # Database connection parameters
    db_params = {
        'dbname': 'cs348proj',
        'user': 'cs348',
        'password': 'cs348',
        'host': '132.145.98.138',
        'port': '5432'
    }

    # Connect to the PostgreSQL database
    print("Attempting to connect to the database...")
    connection = psycopg2.connect(**db_params)
    print("Connection established.")
    cursor = connection.cursor()

    # try:
    #     insert_user_query = """
    #     INSERT INTO ServiceUser (user_id, username, email, password)
    #     VALUES (%s, %s, %s, %s)
    #     RETURNING user_id
    #     """
    #     cursor.execute(insert_user_query, (user_data['user_id'], user_data['username'], user_data['email'], user_data['password']))
    #     user_id = cursor.fetchone()[0]
    # except:
    #     user_id = 1
    # Insert problems    #
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
