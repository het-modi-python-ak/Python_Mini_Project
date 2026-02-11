from config.db import connection
from Models.task import Task




def add_task(task: Task):
    
    info = task.model_dump()

    sql_query = """
                    INSERT INTO tasks (title, description, start_date, due_date, status)
                    VALUES (%(title)s, %(description)s, %(start_date)s, %(due_date)s, %(status)s)
                """
    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query, info)
    except Exception as e:
        print(e)

