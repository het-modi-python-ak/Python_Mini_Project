import json
import os
from Models.task import Task


def save_to_file(filename,tasks):
    """Converts task objects into a dictionary format and writes to a JSON file."""
    data = {}
    for task_id, task in tasks.items():
        data[task_id] = {
            "title": task.title,
            "description": task.description,
            "start_date": task.start_date,
            "due_date": task.due_date,
            "status": task.status,
        }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_from_file(filename,tasks):
    """Reads the JSON file and reconstructs Task objects."""
    if not os.path.exists(filename):
        return

    with open(filename, "r") as f:
        data = json.load(f)

    for task_id, task_data in data.items():
        task_id = int(task_id)
        task = Task(
            task_data["title"],
            task_data["description"],
            task_data["start_date"],
            task_data["due_date"],
            task_data["status"],
            task_id=task_id,
        )
        tasks[task_id] = task

    # Ensure Task._task_id is higher than the highest loaded ID
    if tasks:
        Task._task_id = max(tasks.keys()) + 1

