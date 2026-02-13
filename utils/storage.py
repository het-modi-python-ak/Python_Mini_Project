from models.task import Task
from utils.db import get_connection

# Saves all tasks into PostgreSQL
def save_to_db(tasks):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM tasks")

    for task in tasks.values():
        cur.execute("""
            INSERT INTO tasks (id, title, description, start_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            task.id,
            task.title,
            task.description,
            task.start_date,
            task.due_date,
            task.status
        ))

    conn.commit()
    cur.close()
    conn.close()

# Loads tasks from PostgreSQL
def load_from_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, title, description, start_date, due_date, status FROM tasks")

    rows = cur.fetchall()

    tasks = {}

    for row in rows:
        task = Task(
            row[1],
            row[2],
            row[3],
            row[4],
            row[5],
            task_id=row[0]
        )
        tasks[row[0]] = task

    cur.close()
    conn.close()

    return tasks
