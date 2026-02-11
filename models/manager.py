
from utils.storage import *
from models.task import Task

# --- CLASS DEFINITION: THE LOGIC CONTROLLER ---
class TaskManager:
    def __init__(self, filename="tasks.json"):
        """Sets up the manager and loads existing tasks from disk."""
        self.tasks = {} # Dictionary to store task objects {id: task_obj}
        self.filename = filename
        load_from_file(self.filename)

    def add_task(self, title, description, start_date, due_date, status="Pending"):
        """Creates a new Task object, stores it, and saves to file."""
        try:
            task = Task(title, description, start_date, due_date, status)
            self.tasks[task.id] = task
            save_to_file(self.filename,self.tasks)
            print(f" Task added with ID {task.id}")
        except Exception as e:
            print(f"error in add_task {e}")

    def update_task(self, task_id, **kwargs):
        """Finds a task by ID and applies updates."""
        try:
            if task_id in self.tasks:
                self.tasks[task_id].update_task(**kwargs)
                save_to_file(self.filename,self.tasks)
                print("Task updated successfully")
            else:
                print(":x: Task not found")
        except Exception as e:
            print(f"error in update_task {e}")

    def delete_task(self, task_id):
        """Removes a task from the dictionary and updates the file."""
        try:
            if task_id in self.tasks:
                del self.tasks[task_id]
                save_to_file(self.filename,self.tasks)
                print("Task deleted successfully")
            else:
                print(":x: Task not found")
        except Exception as e:
            print(f"error in delete_task {e}")

    def view_tasks(self):
        """Prints all currently stored tasks."""
        try:
            if not self.tasks:
                print("No tasks available")
                return
            for task in self.tasks.values():
                print(task)
        except Exception as e:
            print(f"error in view_task {e}")
            
    def mark_completed(self, tid):
        try:
            if tid in self.tasks:
                self.tasks[tid].status = "Completed"
                save_to_file(self.filename,self.tasks)
                return True
            return False

        except Exception as e:
            print(f"error in mark_complete {e}")
