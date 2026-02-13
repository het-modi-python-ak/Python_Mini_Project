import asyncio
from datetime import datetime
from Data.database import Database
from task_manager import TaskManager
from Utils.reminder import reminder_loop
from Utils.utils import validate_date


async def main():
    db = Database()
    manager = TaskManager(db)

    asyncio.create_task(reminder_loop(manager))

    try:
        while True:
            print("\n" + "—"*15 + " TASK MANAGER " + "—"*15)
            print(" [1] Add Task      [2] Update Task")
            print(" [3] Delete Task   [4] View All")
            print(" [5] Mark complete [6] Exit")

            choice = await asyncio.to_thread(input, "Choice: ")

            if choice == "1":
                title = input("Title: ")
                desc = input("Description: ")

                while True:
                    due_raw = input("Due Date (YYYY-MM-DD HH:MM): ")
                    date_obj, error = validate_date(due_raw)
                    if date_obj:
                        due = date_obj
                        break
                    print(error)

                start = datetime.now()
                manager.add_task(title, desc, start, due)

            elif choice == "2":
                tid = int(input("Task ID: "))
                new_title = input("New Title (leave blank): ")
                new_status = input("New Status (leave blank): ")

                manager.update_task(
                    tid,
                    title=new_title if new_title else None,
                    status=new_status if new_status else None
                )

            elif choice == "3":
                tid = int(input("Task ID: "))
                manager.delete_task(tid)

            elif choice == "4":
                manager.view_tasks()

            elif choice == "5":
                tid = int(input("Task ID: "))
                if not manager.mark_completed(tid):
                    print("Task not found")

            elif choice == "6":
                print(":wave: Exiting...")
                break

            else:
                print("Invalid choice")

    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(main())