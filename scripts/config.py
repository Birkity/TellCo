import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="PostgreSQL Database Operations")
    parser.add_argument("--host", required=True, help="Database host")
    parser.add_argument("--port", type=int, default=5432, help="Database port")
    parser.add_argument("--database", required=True, help="Database name")
    parser.add_argument("--username", required=True, help="Database username")
    parser.add_argument("--password", required=True, help="Database password")
    return parser.parse_args()

def load_config():
    args = parse_arguments()
    return {
        "host": args.host,
        "port": args.port,
        "database": args.database,
        "username": args.username,
        "password": args.password
    }
