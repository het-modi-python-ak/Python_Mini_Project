
from models.task import Task
from utils.storage import save_to_db, load_from_db
from utils.db import initialize_db

# Handles task lifecycle using database storage
class TaskManager:

    def __init__(self):
        initialize_db()
        self.tasks = load_from_db()

    # Adds new task
    def add_task(self, title, description, start_date, due_date, status="Pending"):
        task = Task(title, description, start_date, due_date, status)
        self.tasks[task.id] = task
        save_to_db(self.tasks)
        print(f"Task added with ID {task.id}")

    # Updates task
    def update_task(self, task_id, **kwargs):
        if task_id in self.tasks:
            self.tasks[task_id].update_task(**kwargs)
            save_to_db(self.tasks)
            print("Task updated successfully")
        else:
            print("Task not found")

    # Deletes task
    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            save_to_db(self.tasks)
            print("Task deleted successfully")
        else:
            print("Task not found")

    # Displays tasks
    def view_tasks(self):
        if not self.tasks:
            print("No tasks available")
            return
        for task in self.tasks.values():
            print(task)

    # Marks task complete
    def mark_completed(self, tid):
        if tid in self.tasks:
            self.tasks[tid].status = "Completed"
            save_to_db(self.tasks)
            return True
        return False
