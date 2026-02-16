from mysql.connector import Error
from datetime import datetime


class TaskManager:
    def __init__(self, db):
        self.db = db

    def add_task(self, title, description, start_date, due_date, status="Pending"):
        try:
            query = """
            INSERT INTO tasks (title, description, start_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.db.cursor.execute(query, (title, description, start_date, due_date, status))
            self.db.commit()
            print(f":white_check_mark: Task added with ID {self.db.cursor.lastrowid}")
        except Error as e:
            self.db.rollback()
            print(f":x: Error adding task: {e}")

    def update_task(self, task_id, **kwargs):
        try:
            updates = []
            values = []

            for key, value in kwargs.items():
                if value is not None:
                    updates.append(f"{key} = %s")
                    values.append(value)

            if not updates:
                print("Nothing to update.")
                return

            query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
            values.append(task_id)

            self.db.cursor.execute(query, values)
            self.db.commit()

            if self.db.cursor.rowcount:
                print(":white_check_mark: Task updated")
            else:
                print(":x: Task not found")

        except Error as e:
            self.db.rollback()
            print(f":x: Update error: {e}")

    def delete_task(self, task_id):
        try:
            self.db.cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            self.db.commit()

            if self.db.cursor.rowcount:
                print(":white_check_mark: Task deleted")
            else:
                print(":x: Task not found")

        except Error as e:
            self.db.rollback()
            print(f":x: Delete error: {e}")

    def view_tasks(self):
        try:
            self.db.cursor.execute("SELECT * FROM tasks ORDER BY due_date")
            tasks = self.db.cursor.fetchall()

            if not tasks:
                print("No tasks available")
                return

            for t in tasks:
                print(
                    f"ID: {t['id']} | "
                    f"Title: {t['title']} | "
                    f"Status: {t['status']} | "
                    f"Start: {t['start_date']} | "
                    f"Due: {t['due_date']}"
                )

        except Error as e:
            print(f":x: View error: {e}")

    def mark_completed(self, task_id):
        try:
            self.db.cursor.execute(
                "UPDATE tasks SET status='Completed' WHERE id=%s",
                (task_id,)
            )
            self.db.commit()
            return self.db.cursor.rowcount > 0
        except Error as e:
            self.db.rollback()
            print(f":x: Complete error: {e}")
            return False

    def get_all_tasks(self):
        try:
            self.db.cursor.execute("SELECT * FROM tasks")
            return self.db.cursor.fetchall()
        except Error:
            return []