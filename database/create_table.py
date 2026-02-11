from config.db import connection

sql_query = ("""
             CREATE TABLE IF NOT EXISTS Tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                description VARCHAR(200),
                start_date DATE DEFAULT CURRENT_DATE,
                due_date DATE,
                status VARCHAR(50)
            );
             """)


with connection() as conn:
    with conn.cursor() as cur:
        try:
            cur.execute(sql_query)
            
        except Exception as e:
            print(e)
            