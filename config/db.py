import os
import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv()

conn_params = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DATABASE"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "port": os.getenv("DB_PORT"),
}

@contextmanager
def connection():
    try:
        conn = psycopg2.connect(**conn_params)
        yield conn
        conn.commit()
    except Error as e:
        conn.rollback()
        print(f"Error {e}")
    finally:
        conn.close()



