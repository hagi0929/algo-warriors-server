import json
import psycopg2
from dotenv import dotenv_values


env_vars = dotenv_values('.env')



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



def execute_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor



def user_exists(conn, user_id):
    query = "SELECT 1 FROM ServiceUser WHERE user_id = %s"
    cursor = execute_query(conn, query, (user_id,))
    return cursor.fetchone() is not None



def populate_users_from_json(json_file, conn):
    
    with open(json_file, 'r') as f:
        users = json.load(f)

    
    for user in users:
        if not user_exists(conn, user['user_id']):
            query = """
            INSERT INTO ServiceUser (user_id, username, role_id, email, password, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """
            params = (user['user_id'], user['username'], user['role_id'], user['email'], user['password'])
            execute_query(conn, query, params)

    
    conn.commit()
    print("Users have been populated successfully.")



if __name__ == "__main__":
    users_json_file = 'users.json'

    
    connection = connect_db()
    if connection:
        try:
            
            populate_users_from_json(users_json_file, connection)
        finally:
            
            connection.close()
            print("Connection closed.")
