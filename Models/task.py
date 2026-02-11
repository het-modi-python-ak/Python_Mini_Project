class Task:
    _task_id = 1

    @classmethod
    def generate_id(cls):
        """Increments and returns a unique ID for new tasks."""
        tsk_id = cls._task_id
        cls._task_id += 1
        return tsk_id

    def __init__(
        self, title, description, start_date, due_date, status="Pending", task_id=None
    ):
        """Initializes a new task instance. Handles both new and loaded tasks."""
        if task_id is not None:
            self.id = task_id  # Use existing ID (for loading from file)
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
