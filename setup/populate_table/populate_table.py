import psycopg2
import bcrypt
import random
import string
import json
from dotenv import load_dotenv, find_dotenv
import os


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print(files)
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

def insert_data():
    user_data = read_json_file('setup/populate_table/users.json')

    connection = psycopg2.connect(
    )
    # cursor = connection.cursor()
    
    # # Insert admin user from JSON data
    # username = user_data['username']
    # email = user_data['email']
    # hashed_password = user_data['password']
    
    # insert_user_query = """
    # INSERT INTO ServiceUser (username, email, password)
    # VALUES (%s, %s, %s)
    # RETURNING user_id
    # """
    # cursor.execute(insert_user_query, (username, email, hashed_password))
    # user_id = cursor.fetchone()[0]
    
    # # Insert problem
    # problem_title = 'Example Problem'
    # problem_description = 'This is an example problem description.'
    # problem_difficulty = 10
    
    # insert_problem_query = """
    # INSERT INTO Problem (title, description, difficulty, created_by)
    # VALUES (%s, %s, %s, %s)
    # RETURNING problem_id
    # """
    # cursor.execute(insert_problem_query, (problem_title, problem_description, problem_difficulty, user_id))
    # problem_id = cursor.fetchone()[0]
    
    # # Insert test cases
    # test_cases = [
    #     (problem_id, True, 'input1', 'output1'),
    #     (problem_id, True, 'input2', 'output2'),
    #     (problem_id, False, 'input3', 'output3')
    # ]
    
    # insert_test_case_query = """
    # INSERT INTO TestCase (problem_id, is_public, input, output)
    # VALUES (%s, %s, %s, %s)
    # """
    # cursor.executemany(insert_test_case_query, test_cases)
    
    # # Commit the transaction
    # connection.commit()
    
    # print(f"Admin user added with email: {email}")
    # print(f"Problem added with title: {problem_title}")
    # print("Test cases added for the problem.")
    # if connection:
    #     cursor.close()
    #     connection.close()

if __name__ == "__main__":
    insert_data()
