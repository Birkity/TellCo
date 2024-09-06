import os
from .db_connection import establish_connection

def load_schema(conn, schema_path):
    with open(schema_path, 'r') as schema_file:
        schema_sql = schema_file.read()
    
    try:
        cur = conn.cursor()
        cur.execute(schema_sql)
        conn.commit()
        print("Schema executed successfully.")
    except Exception as e:
        print(f"Error executing schema: {e}")
        conn.rollback()
        raise

def execute_schema(conn, schema_path):
    conn = establish_connection({"host": "localhost", "port": 5432, "database": "your_database", "username": "your_user", "password": "your_password"})
    load_schema(conn, schema_path)
