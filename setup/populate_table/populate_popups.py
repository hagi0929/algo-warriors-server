import pandas as pd
from sqlalchemy import create_engine, text

# Database connection URL
DATABASE_URI = 'postgresql+psycopg2://cs348:cs348@132.145.98.138:5432/cs348proj'
engine = create_engine(DATABASE_URI)

# Read the dataset
csv_path = 'setup/populate_table/repositories.csv'
df = pd.read_csv(csv_path)

# Insert data into the database
with engine.connect() as connection:
    for index, row in df.iterrows():
        sql = text('''
            INSERT INTO PopupResource (resource_name, resource_description, resource_url, homepage, size, stars, forks, issues)
            VALUES (:resource_name, :resource_description, :resource_url, :homepage, :size, :stars, :forks, :issues)
        ''')
        connection.execute(sql, {
            'resource_name': row['Name'],
            'resource_description': row['Description'],
            'resource_url': row['URL'],
            'homepage': row['Homepage'],
            'size': row['Size'],
            'stars': row['Stars'],
            'forks': row['Forks'],
            'issues': row['Issues']
        })

print("Data insertion complete.")
