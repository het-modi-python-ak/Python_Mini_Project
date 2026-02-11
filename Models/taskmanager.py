from Models.task import Task
from utils.file_handler import load_from_file, save_to_file


class TaskManager:
    _id = 0
    @classmethod
    def get_id(cls):
        cls._id = cls._id +1
        return cls._id

    def __init__(self, filename="data/tasks.json"):
        """Sets up the manager and loads existing tasks from disk."""
        self.tasks = {} 
        self.filename = filename
        load_from_file(self.filename,self.tasks)
        

    def add_task(self, title, description, due_date,):
        """Creates a new Task object, stores it, and saves to file."""
        task = Task(id = TaskManager.get_id(),title = title, description=description, due_date=due_date)
        self.tasks[task.id] = task.model_dump(exclude=['id'])
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

    
