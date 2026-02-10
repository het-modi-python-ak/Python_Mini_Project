import asyncio
import json
import os
from datetime import datetime
# --- CLASS DEFINITION: THE DATA MODEL ---
class Task:
    # Class-level variable to keep track of the next unique ID
    task_id_counter = 1

    @classmethod
    def generate_id(cls):
        """Increments and returns a unique ID for new tasks."""
        tsk_id = cls.task_id_counter
        cls.task_id_counter += 1
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
        print(f" Task added with ID {task.id}")

    def update_task(self, task_id, **kwargs):
        """Finds a task by ID and applies updates."""
        if task_id in self.tasks:
            self.tasks[task_id].update_task(**kwargs)
            self.save_to_file()
            print("Task updated successfully")
        else:
            print(":x: Task not found")

    def delete_task(self, task_id):
        """Removes a task from the dictionary and updates the file."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_to_file()
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
            self.save_to_file()
            return True
        return False

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

        # Ensure Task.task_id_counter is higher than the highest loaded ID
        if self.tasks:
            Task.task_id_counter = max(self.tasks.keys()) + 1


def validate_date(date_text):
    """Validates date format and ensures it is in the future."""
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d %H:%M")
        if date_obj < datetime.now():
            return None, "Due date must be in the future!"
        return date_obj, None
    except ValueError:
        return None, "Invalid format! Use YYYY-MM-DD HH:MM"


async def reminder_loop(manager):
    """Prints urgent sorted tasks every 10s without breaking the UI."""
    while True:
        await asyncio.sleep(10)
        # Sort pending tasks by due date
        pending = [t for t in manager.tasks.values() if t.status.lower() != "completed"]
        pending.sort(key=lambda x: datetime.strptime(x.due_date, "%Y-%m-%d %H:%M"))

        if pending:
            # \r\033[K clears the current input line, \033[1;33m is Yellow Bold
            print(f"\r\033[K\n\033[1;33m{'='*40}\n🔔 URGENT REMINDERS (Sorted by Due Date)\n{'-'*40}")
            for t in pending[:3]: # Show top 3 most urgent
                print(f"{t.id} ⚠️ {t.due_date} -> {t.title}")
            print(f"{'='*40}\033[0m")
            print("Choice: ", end="", flush=True)
            

# --- ENTRY POINT: USER INTERFACE ---
async def main():
    manager = TaskManager()
    asyncio.create_task(reminder_loop(manager))
    
    while True:
        print("\n\033[1;36m" + "—"*15 + " TASK MANAGER " + "—"*15 + "\033[0m")
        print(" [1] Add Task      [2] Update Task")
        print(" [3] Delete Task   [4] View All")
        print(" [5] Mark complete [6] Exit")

        choice = await asyncio.to_thread(input,'Choice: ')

        # Handle user menu selections
        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            while True:
                due_raw = input("Due Date (YYYY-MM-DD HH:MM): ")
                date_obj, error = validate_date(due_raw)
                if date_obj:
                    due = due_raw
                    break
                print(f"❌ {error}")
            
            start = datetime.now().strftime("%Y-%m-%d %H:%M")
            manager.add_task(title, desc, start, due)

        elif choice == "2":
            try:
                tid = int(input("Task ID: "))
                new_title = input("New Title (leave blank): ")
                new_status = input("New Status (e.g. Done): ")
                manager.update_task(tid, 
                    title=new_title if new_title else None, 
                    status=new_status if new_status else None)
            except ValueError: print("❌ Enter a numeric ID.")   

        elif choice == "3":
            try:
                tid = int(input("Task ID to delete: "))
                manager.delete_task(tid)
            except ValueError: print("❌ Invalid ID.")
        
        elif choice == "4":
            manager.view_tasks()

        elif choice =="5":
            try:
                tid = int(input("Task ID to Mark as completed: "))
                manager.mark_completed(tid)
            except ValueError: print("❌ Invalid ID.")
            
        elif choice == "6":
            print(":wave: Exiting Task Manager")
            break

        else:
            print(":x: Invalid choice")

# Ensure the main function only runs if the script is executed directly
if __name__ == "__main__":
    asyncio.run(main())