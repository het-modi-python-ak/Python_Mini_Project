class Task:
    _id_ct = 1
    
    @classmethod
    def generate_id(cls):
        tsk_id = cls._id_ct
        cls._id_ct += 1
        return tsk_id

    def __init__(self, title, description, start_date, due_date, status="Pending"):
        self.id = Task.generate_id()
        self.title = title
        self.start_date = start_date
        self.due_date = due_date
        self.description = description
        self.status = status

    def update_task(self, title=None, description=None, start_date=None, due_date=None, status=None):
        if title: self.title = title
        if description: self.description = description
        if start_date: self.start_date = start_date
        if due_date: self.due_date = due_date
        if status: self.status = status

   
    def __str__(self):
        return f"ID: {self.id} | {self.title} | Status: {self.status}"

class Taskmng:
    def __init__(self):
        self.tasks = {}

    def add_task(self, title, description, start_date, due_date, status="Pending"):
        task = Task(title, description, start_date, due_date, status)
        
        self.tasks[task.id] = task 
        print("Successfully added task", task.id)

    def update_task(self, task_id, **kwargs):
        if task_id in self.tasks:
            task = self.tasks[task_id]
           
            task.update_task(**kwargs)
            print("Task updated successfully")
        else:
            print("Task not found")

    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            print("Task deleted succesfully")
        else:
            print("Task not found")

    def view_task(self):
        if not self.tasks:
            print("No task found")
            return
        
        for task in self.tasks.values():
           
            print(task)


mng = Taskmng()
mng.add_task("Complete task", "this is description", "12-09-2004", "13-09-1009", "Pending")
mng.add_task("Complete task", "this is description", "12-09-2004", "13-09-1009", "Pending")
mng.view_task()

mng.update_task(1,title="Chenage title")
mng.view_task()
mng.delete_task(1)
mng.view_task()