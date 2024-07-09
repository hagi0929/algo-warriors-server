# Description: Python script to populate the PopupResource table in the database with data from a CSV file.
# Author: Vidhi Ruparel
import pandas as pd
import psycopg2
from psycopg2 import sql
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')

# Function to connect to PostgreSQL database
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

# Function to execute SQL queries and return results
def execute_query(conn, query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor

# Function to insert data into PopupResource table
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

# Main function to process the CSV file and populate the database
def process_csv_file(csv_file, conn):
    # Read CSV data
    df = pd.read_csv(csv_file)
    
    # Process each row
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

    # Commit changes
    conn.commit()

# Execute the script
if __name__ == "__main__":
    csv_file_path = 'setup/populate_table/repositories.csv'
    
    # Connect to PostgreSQL database
    connection = connect_db()
    if connection:
        try:
            # Process CSV file and populate database
            process_csv_file(csv_file_path, connection)
        finally:
            # Close connection
            connection.close()
            print("Connection closed.")
