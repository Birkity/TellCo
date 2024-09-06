import psycopg2
from .db_connection import establish_connection

def execute_query(conn, query):
    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except Exception as e:
        print(f"Error executing query: {e}")
        raise

def fetch_results(conn, query):
    conn = establish_connection({"host": "localhost", "port": 5432, "database": "your_database", "username": "your_user", "password": "your_password"})
    return execute_query(conn, query)
