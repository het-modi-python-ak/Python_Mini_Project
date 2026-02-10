from utils.storage import save_to_file, load_from_file
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
        task = Task(title, description, start_date, due_date, status)
        self.tasks[task.id] = task
        save_to_file(self.filename,self.tasks)
        print(f" Task added with ID {task.id}")

    def update_task(self, task_id, **kwargs):
        """Finds a task by ID and applies updates."""
        if task_id in self.tasks:
            self.tasks[task_id].update_task(**kwargs)
            save_to_file(self.filename,self.tasks)
            print("Task updated successfully")
        else:
            print(":x: Task not found")

    def delete_task(self, task_id):
        """Removes a task from the dictionary and updates the file."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            save_to_file(self.filename,self.tasks)
            print("Task deleted successfully")
        else:
            print(":x: Task not found")

    def view_tasks(self):
        """Prints all currently stored tasks."""
        if not self.tasks:
            print("No tasks available")
            return
        for task in self.tasks.values():
            print(task)
            
    def mark_completed(self, tid):
        if tid in self.tasks:
            self.tasks[tid].status = "Completed"
            save_to_file(self.filename,self.tasks)
            return True
        return False