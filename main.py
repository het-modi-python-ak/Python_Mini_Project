import json
import os

# --- CLASS DEFINITION: THE DATA MODEL ---
class Task:
    # Class-level variable to keep track of the next unique ID
    _id_ct = 1

    @classmethod
    def generate_id(cls):
        """Increments and returns a unique ID for new tasks."""
        tsk_id = cls._id_ct
        cls._id_ct += 1
        return tsk_id

    def __init__(self, title, description, start_date, due_date, status="Pending", task_id=None):
        """Initializes a new task instance. Handles both new and loaded tasks."""
        if task_id is not None:
            self.id = task_id # Use existing ID (for loading from file)
        else:
            self.id = Task.generate_id()  # Generate new ID (for new tasks)

        self.title = title
        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.status = status

    def update_task(self, **kwargs):
        """Updates specific attributes dynamically using key-value pairs."""
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        """Defines how the task looks when printed."""
        return (
            f"ID: {self.id} | "
            f"Title: {self.title} | "
            f"Status: {self.status} | "
            f"Start: {self.start_date} | "
            f"Due: {self.due_date}"
        )

# --- CLASS DEFINITION: THE LOGIC CONTROLLER ---
class TaskManager:
    def __init__(self, filename="tasks.json"):
        """Sets up the manager and loads existing tasks from disk."""
        self.tasks = {} # Dictionary to store task objects {id: task_obj}
        self.filename = filename
        self.load_from_file()

    def add_task(self, title, description, start_date, due_date, status="Pending"):
        """Creates a new Task object, stores it, and saves to file."""
        task = Task(title, description, start_date, due_date, status)
        self.tasks[task.id] = task
        self.save_to_file()
        print(f":white_check_mark: Task added with ID {task.id}")

    def update_task(self, task_id, **kwargs):
        """Finds a task by ID and applies updates."""
        if task_id in self.tasks:
            self.tasks[task_id].update_task(**kwargs)
            self.save_to_file()
            print(":white_check_mark: Task updated successfully")
        else:
            print(":x: Task not found")

    def delete_task(self, task_id):
        """Removes a task from the dictionary and updates the file."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_to_file()
            print(":white_check_mark: Task deleted successfully")
        else:
            print(":x: Task not found")

    def view_tasks(self):
        """Prints all currently stored tasks."""
        if not self.tasks:
            print(":warning: No tasks available")
            return
        for task in self.tasks.values():
            print(task)

    def save_to_file(self):
        """Converts task objects into a dictionary format and writes to a JSON file."""
        data = {}
        for task_id, task in self.tasks.items():
            data[task_id] = {
                "title": task.title,
                "description": task.description,
                "start_date": task.start_date,
                "due_date": task.due_date,
                "status": task.status
            }

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self):
        """Reads the JSON file and reconstructs Task objects."""
        if not os.path.exists(self.filename):
            return

        with open(self.filename, "r") as f:
            data = json.load(f)

        for task_id, task_data in data.items():
            task_id = int(task_id)
            task = Task(
                task_data["title"],
                task_data["description"],
                task_data["start_date"],
                task_data["due_date"],
                task_data["status"],
                task_id=task_id
            )
            self.tasks[task_id] = task

        # Ensure Task._id_ct is higher than the highest loaded ID
        if self.tasks:
            Task._id_ct = max(self.tasks.keys()) + 1


# --- ENTRY POINT: USER INTERFACE ---
def main():
    manager = TaskManager()

    while True:
        print("\n--- TASK MANAGER ---")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        # Handle user menu selections
        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            start = input("Start Date: ")
            due = input("Due Date: ")
            status = input("Status (Pending/Completed): ") or "Pending"
            manager.add_task(title, desc, start, due, status)

        elif choice == "2":
            try:
                task_id = int(input("Task ID: "))
                title = input("New Title (leave blank to skip): ")
                status = input("New Status (leave blank to skip): ")

                manager.update_task(
                    task_id,
                    title=title if title else None,
                    status=status if status else None
                )
            except ValueError:
                print(":x: Please enter a valid numeric ID")   

        elif choice == "3":
            try:
                task_id = int(input("Task ID: "))
                manager.delete_task(task_id)
            except ValueError:
                print(":x: Please enter a valid numeric ID")

        elif choice == "4":
            manager.view_tasks()

        elif choice == "5":
            print(":wave: Exiting Task Manager")
            break

        else:
            print(":x: Invalid choice")

# Ensure the main function only runs if the script is executed directly
if __name__ == "__main__":
    main()