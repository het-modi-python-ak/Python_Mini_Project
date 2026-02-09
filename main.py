import json
import os


class Task:
    _id_ct = 1

    @classmethod
    def generate_id(cls):
        tsk_id = cls._id_ct
        cls._id_ct += 1
        return tsk_id

    def __init__(self, title, description, start_date, due_date, status="Pending", task_id=None):
        if task_id is not None:
            self.id = task_id
        else:
            self.id = Task.generate_id()

        self.title = title
        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.status = status

    def update_task(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

    def __str__(self):
        return (
            f"ID: {self.id} | "
            f"Title: {self.title} | "
            f"Status: {self.status} | "
            f"Start: {self.start_date} | "
            f"Due: {self.due_date}"
        )


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.tasks = {}
        self.filename = filename
        self.load_from_file()

    def add_task(self, title, description, start_date, due_date, status="Pending"):
        task = Task(title, description, start_date, due_date, status)
        self.tasks[task.id] = task
        self.save_to_file()
        print(f":white_check_mark: Task added with ID {task.id}")

    def update_task(self, task_id, **kwargs):
        if task_id in self.tasks:
            self.tasks[task_id].update_task(**kwargs)
            self.save_to_file()
            print(":white_check_mark: Task updated successfully")
        else:
            print(":x: Task not found")

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            self.save_to_file()
            print(":white_check_mark: Task deleted successfully")
        else:
            print(":x: Task not found")

    def view_tasks(self):
        if not self.tasks:
            print(":warning: No tasks available")
            return
        for task in self.tasks.values():
            print(task)

    def save_to_file(self):
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

        if self.tasks:
            Task._id_ct = max(self.tasks.keys()) + 1


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

        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            start = input("Start Date: ")
            due = input("Due Date: ")
            status = input("Status (Pending/Completed): ") or "Pending"
            manager.add_task(title, desc, start, due, status)

        elif choice == "2":
            task_id = int(input("Task ID: "))
            title = input("New Title (leave blank to skip): ")
            status = input("New Status (leave blank to skip): ")

            manager.update_task(
                task_id,
                title=title if title else None,
                status=status if status else None
            )

        elif choice == "3":
            task_id = int(input("Task ID: "))
            manager.delete_task(task_id)

        elif choice == "4":
            manager.view_tasks()

        elif choice == "5":
            print(":wave: Exiting Task Manager")
            break

        else:
            print(":x: Invalid choice")


if __name__ == "__main__":
    main()