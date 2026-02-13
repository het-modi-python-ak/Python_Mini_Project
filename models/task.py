# Represents a task and handles ID generation
class Task:

    task_id_counter = 1

    # Generates unique task IDs
    @classmethod
    def generate_id(cls):
        task_id = cls.task_id_counter
        cls.task_id_counter += 1
        return task_id

    # Creates a new task object
    def __init__(self, title, description, start_date, due_date, status="Pending", task_id=None):
        self.id = task_id if task_id is not None else Task.generate_id()
        self.title = title
        self.description = description
        self.start_date = start_date
        self.due_date = due_date
        self.status = status

    # Updates selected fields of a task
    def update_task(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

    # Formats task for printing
    # def __str__(self):
    #     return f"ID: {self.id} | Title: {self.title} | Status: {self.status} | Start: {self.start_date} | Due: {self.due_date}”
    def __str__(self):
        """Defines how the task looks when printed."""
        return (
            f"ID: {self.id} | "
            f"Title: {self.title} | "
            f"Status: {self.status} | "
            f"Start: {self.start_date} | "
            f"Due: {self.due_date}"
        )
    