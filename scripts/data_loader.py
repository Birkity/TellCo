import psycopg2
from .db_connection import establish_connection

def load_data(conn, sql_path):
    try:
        with open(sql_path, 'r') as sql_file:
            sql_query = sql_file.read()
        
        cur = conn.cursor()
        cur.execute(sql_query)
        conn.commit()
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
        conn.rollback()
        raise

def execute_load_data(conn, sql_path):
    conn = establish_connection({"host": "localhost", "port": 5432, "database": "your_database", "username": "your_user", "password": "your_password"})
    load_data(conn, sql_path)
