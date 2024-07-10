

import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import dotenv_values


env_vars = dotenv_values('.env')


def connect_db():
    conn_params = {
        'dbname': env_vars['DB_DATABASE_DEV'],
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


def insert_resource(conn, resource):
    query = sql.SQL('''
        INSERT INTO PopupResource (
            resource_name, resource_description, resource_url, created_at, updated_at, homepage,
            size, stars, forks, issues, watchers, resource_language, license, topics, has_issues, 
            has_projects, has_downloads, has_wiki, has_pages, has_discussions, is_fork, 
            is_archived, is_template, default_branch
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    ''')
    execute_query(conn, query, (
        resource['Name'],
        resource['Description'],
        resource['URL'],
        resource['Created At'],
        resource['Updated At'],
        resource['Homepage'],
        resource['Size'],
        resource['Stars'],
        resource['Forks'],
        resource['Issues'],
        resource['Watchers'],
        resource['Language'],
        resource['License'],
        resource['Topics'],
        resource['Has Issues'],
        resource['Has Projects'],
        resource['Has Downloads'],
        resource['Has Wiki'],
        resource['Has Pages'],
        resource['Has Discussions'],
        resource['Is Fork'],
        resource['Is Archived'],
        resource['Is Template'],
        resource['Default Branch']
    ))


def process_csv_file(csv_file, conn):
    
    df = pd.read_csv(csv_file)
    
    
    i = 0
    for index, row in df.iterrows():
        if i > 10000:
            break
        print(f"Inserting row {index + 1}: {row['Name']}, {row['Description']}, {row['URL']}, {row['Homepage']}, {row['Size']}, {row['Stars']}, {row['Forks']}, {row['Issues']}")
        try:
            insert_resource(conn, row)
            print(f"Row {index + 1} inserted successfully.")
        except Exception as e:
            print(f"Error inserting row {index + 1}: {e}")
        i += 1

    
    conn.commit()


if __name__ == "__main__":
    csv_file_path = 'setup/populate_table/repositories.csv'
    
    
    connection = connect_db()
    if connection:
        try:
            
            process_csv_file(csv_file_path, connection)
        finally:
            
            connection.close()
            print("Connection closed.")
