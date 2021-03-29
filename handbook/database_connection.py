import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str) -> psycopg2.connect:
    """
    Creates a connection to the database
    Raises an exception on error
    """
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
    except OperationalError as e:
        print(e)
    return connection
