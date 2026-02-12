from config.db import connection
from Models.task import Task, UpdateTask


def add_task(task: Task):

    info = task.model_dump()

    sql_query = """
                    INSERT INTO tasks (title, description, start_date, due_date, status)
                    VALUES (%(title)s, %(description)s, %(start_date)s, %(due_date)s, %(status)s)
                    RETURNING id
                """
    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query, info)
                task_id_tuple = cur.fetchone()

                if task_id_tuple:
                    task_id = task_id_tuple[0]
                    print(f"Task successfully inserted with ID: {task_id}")
                else:
                    print("Failed to retrieve the inserted task ID.")
                return task_id
    except Exception as e:
        print(e)


def delete_task(task_id: int):
    sql_query = """
                    DELETE FROM tasks as t
                    WHERE t.id = %s
                """
    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query, (task_id,))
                if cur.rowcount == 0:
                    print(f"No task found with id {task_id}")
                else:
                    print(f"Task {task_id} deleted successfully.")

    except Exception as e:
        print(e)


def update_task(task_id: int, task_data: UpdateTask):
    update_data = task_data.model_dump(exclude_none=True)

    if not update_data:
        print("No fields provided for update.")
        return

    set_clause = ", ".join([f"{key} = %({key})s" for key in update_data.keys()])
    sql_query = f"UPDATE tasks SET {set_clause} WHERE id = %(task_id)s"
    update_data["task_id"] = task_id

    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query, update_data)
                if cur.rowcount == 0:
                    print(f"No task found with id {task_id}")
                else:
                    print(f"Task {task_id} updated successfully.")
    except Exception as e:
        print(f"Error: {e}")


def mark_completed(task_id: int):

    sql_query = """
                    UPDATE tasks
                    SET status = 'Completed'
                    WHERE id = %s
                """

    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query, (task_id,))
                if cur.rowcount == 0:
                    print(f"No task found with id {task_id}")
                else:
                    print(f"Task {task_id} status updated successfully.")
    except Exception as e:
        print(e)


def load():

    sql_query = """
                SELECT id,title,due_date,status from tasks
                """

    try:
        with connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql_query)
                if cur.rowcount == 0:
                    print(f"No task found")
                else:
                    print()
                return cur.fetchall()
    except Exception as e:
        print(e)


