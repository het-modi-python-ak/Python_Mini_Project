from utils.storage import save_to_file, load_from_file
from models.task import Task

# Handles task operations and persistence
class TaskManager:

    # Initializes manager and loads stored tasks
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = load_from_file(self.filename)

    # Adds a new task
    def add_task(self, title, description, start_date, due_date, status="Pending"):
        task = Task(title, description, start_date, due_date, status)
        self.tasks[task.id] = task
        save_to_file(self.filename, self.tasks)
        print(f"Task added with ID {task.id}")

    # Updates an existing task
    def update_task(self, task_id, **kwargs):
        if task_id in self.tasks:
            self.tasks[task_id].update_task(**kwargs)
            save_to_file(self.filename, self.tasks)
            print("Task updated successfully")
        else:
            print("Task not found")

    # Deletes a task
    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            save_to_file(self.filename, self.tasks)
            print("Task deleted successfully")
        else:
            print("Task not found")

    # Displays all tasks
    def view_tasks(self):
        if not self.tasks:
            print("No tasks available")
            return
        for task in self.tasks.values():
            print(task)

    # Marks a task as completed
    def mark_completed(self, tid):
        if tid in self.tasks:
            self.tasks[tid].status = "Completed"
            save_to_file(self.filename, self.tasks)
            return True
        return False
