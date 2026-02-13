import json
import os
from models.task import Task

# Saves tasks to JSON file
def save_to_file(filename, tasks):
    data = {}
    for task_id, task in tasks.items():
        data[task_id] = {
            "title": task.title,
            "description": task.description,
            "start_date": task.start_date,
            "due_date": task.due_date,
            "status": task.status
        }

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Loads tasks from JSON file
def load_from_file(filename):
    tasks = {}

    if not os.path.exists(filename):
        return tasks

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
            task_id=task_id
        )

        tasks[task_id] = task

    if tasks:
        Task.task_id_counter = max(tasks.keys()) + 1

    return tasks