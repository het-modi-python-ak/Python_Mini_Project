import asyncio
from Models.task import Task, UpdateTask
from database import operations
from utils.reminder import reminder_loop



async def main():

    tasks = operations.load()
    asyncio.create_task(reminder_loop(tasks))

    while True:
        print("\n\033[1;36m" + "—" * 15 + " TASK MANAGER " + "—" * 15 + "\033[0m")
        print(" [1] Add Task      [2] Update Task")
        print(" [3] Delete Task   [4] View All")
        print(" [5] Mark complete [6] Exit")

        choice = await asyncio.to_thread(input, "Choice: ")

        if choice == "1":
            try:
                title = input("Title: ")
                desc = input("Description: ")
                due = input("Due date (YYYY-MM-DD): ")
                new_task = Task(title=title, description=desc, due_date=due)
                task_id = operations.add_task(new_task)
                tasks[:] = operations.load() 
            except ValueError as e:
                print(f"❌ Invalid data: {e}")

        elif choice == "2":
            try:
                task_id = int(input("Task ID: "))

                new_title = input("New Title (skip with Enter): ")
                new_status = input("New Status (skip with Enter): ")

                update_data = UpdateTask(
                    title=new_title or None, status=new_status or None
                )
                operations.update_task(task_id, update_data)
                
                tasks[:] = operations.load() 
            except ValueError:
                print("❌ Task ID must be a number.")

        elif choice == "3":
            try:
                task_id = int(input("Task ID to delete: "))
                operations.delete_task(task_id)
                tasks[:] = operations.load() 
            except ValueError:
                print("❌ Invalid ID.")

        elif choice == "4":
            tasks[:] = operations.load() 
            for row in tasks:
                print(f"ID: {row[0]} | Title: {row[1]} | Due: {row[2]}")

        elif choice == "5":
            try:
                tid = int(input("Task ID to Mark as completed: "))
                operations.mark_completed(tid)
                tasks[:] = operations.load() 
            except ValueError:
                print("❌ Invalid ID.")

        elif choice == "6":
            print("👋 Exiting Task Manager")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())
