import json
import os
from Models.task import Task



def save_to_file(filename,tasks):
    """Converts task objects into a dictionary format and writes to a JSON file."""

    with open(filename, "w") as f:
        json.dump(tasks, f, indent=4)


def load_from_file(filename,tasks):
    from Models.taskmanager import TaskManager 
    """Reads the JSON file and reconstructs Task objects."""
    if not os.path.exists(filename):
        return

    with open(filename, "r") as f:
        data = json.load(f)

    for task_id, task_data in data.items():
        task = Task(
            id = task_id,
            title=task_data["title"],
            description=task_data["description"],
            start_date=task_data["start_date"],
            due_date=task_data["due_date"],
            status=task_data["status"]
        )
        tasks[task_id] = task.model_dump(exclude=['id'])

    # Ensure Task._task_id is higher than the highest loaded ID
    if tasks:
        TaskManager._id = max([int(x) for x in tasks.keys()])

