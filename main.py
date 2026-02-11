from Models.taskmanager import TaskManager
from utils.date_validate import validate_date
from utils.reminder import reminder_loop
import asyncio
from datetime import datetime


async def main():
    manager = TaskManager()
    asyncio.create_task(reminder_loop(manager))

    while True:
        print("\n\033[1;36m" + "—" * 15 + " TASK MANAGER " + "—" * 15 + "\033[0m")
        print(" [1] Add Task      [2] Update Task")
        print(" [3] Delete Task   [4] View All")
        print(" [5] Mark complete [6] Exit")

        choice = await asyncio.to_thread(input, "Choice: ")

        # Handle user menu selections
        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            due = input("Due date: ")
            manager.add_task(title, desc, due)

        elif choice == "2":
            try:
                tid = int(input("Task ID: "))
                new_title = input("New Title (leave blank): ")
                new_status = input("New Status (e.g. Done): ")
                manager.update_task(
                    tid,
                    title=new_title if new_title else None,
                    status=new_status if new_status else None,
                )
            except ValueError:
                print("❌ Enter a numeric ID.")

        elif choice == "3":
            try:
                tid = int(input("Task ID to delete: "))
                manager.delete_task(tid)
            except ValueError:
                print("❌ Invalid ID.")

        elif choice == "4":
            manager.view_tasks()

        elif choice == "5":
            try:
                tid = int(input("Task ID to Mark as completed: "))
                manager.mark_completed(tid)
            except ValueError:
                print("❌ Invalid ID.")

        elif choice == "6":
            print(":wave: Exiting Task Manager")
            break

        else:
            print(":x: Invalid choice")


# Ensure the main function only runs if the script is executed directly
if __name__ == "__main__":
    asyncio.run(main())
