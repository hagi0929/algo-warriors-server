import json
import psycopg2
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')


# Function to connect to PostgreSQL database
def connect_db():
    conn_params = {
        'dbname': env_vars['DB_DATABASE'],
        'user': env_vars['DB_USER'],
        'password': env_vars['DB_PASSWORD'],
        'host': env_vars['DB_HOST'],
        'port': env_vars['DB_PORT']
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


# Function to check if user exists
def user_exists(conn, user_id):
    query = "SELECT 1 FROM ServiceUser WHERE user_id = %s"
    cursor = execute_query(conn, query, (user_id,))
    return cursor.fetchone() is not None


# Function to populate ServiceUser table from JSON file
def populate_users_from_json(json_file, conn):
    # Load JSON data
    with open(json_file, 'r') as f:
        users = json.load(f)

    # Insert each user into the ServiceUser table if they do not exist
    for user in users:
        if not user_exists(conn, user['user_id']):
            query = """
            INSERT INTO ServiceUser (user_id, username, role_id, email, password, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """
            params = (user['user_id'], user['username'], user['role_id'], user['email'], user['password'])
            execute_query(conn, query, params)

    # Commit changes
    conn.commit()
    print("Users have been populated successfully.")


# Example usage
if __name__ == "__main__":
    users_json_file = 'users.json'

    # Connect to PostgreSQL database
    connection = connect_db()
    if connection:
        try:
            # Populate ServiceUser table from users.json
            populate_users_from_json(users_json_file, connection)
        finally:
            # Close connection
            connection.close()
            print("Connection closed.")
