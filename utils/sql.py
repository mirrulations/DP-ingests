import psycopg
import os
from common.utils.secrets import get_secret

def connect():
    """
    Create a connection to the PostgreSQL database.
    If running locally, connect to the local PostgreSQL instance.
    If running in AWS, connect to the production PostgreSQL instance.
    """
    if os.environ.get('AWS_SAM_LOCAL'):
        conn_params = {
            "dbname": os.environ.get('POSTGRES_DB'),
            "user": os.environ.get('POSTGRES_USER'),
            "password": os.environ.get('POSTGRES_PASSWORD'),
            "host": os.environ.get('POSTGRES_HOST'),
            "port": os.environ.get('POSTGRES_PORT'),
        }
    else:
        secret_name = os.environ.get('DB_SECRET_NAME')
        secret = get_secret(secret_name)

        conn_params = {
            "dbname": secret['db'],
            "user": secret['username'],
            "password": secret['password'],
            "host": secret['host'],
            "port": secret['port'],
        }

    conn = psycopg.connect(**conn_params)
    return conn
