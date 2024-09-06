import psycopg2
from .config import load_config

def establish_connection(config):
    try:
        conn = psycopg2.connect(
            dbname=config["database"],
            user=config["username"],
            password=config["password"],
            host=config["host"],
            port=config["port"]
        )
        print(f"Connected to: {conn.get_dsn_parameters()}")
        return conn
    except Exception as e:
        print(f"Error establishing connection: {e}")
        raise
