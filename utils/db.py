import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Creates database connection
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),   
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

# Creates tasks table if it does not exist
def initialize_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            start_date TEXT,
            due_date TEXT,
            status TEXT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
