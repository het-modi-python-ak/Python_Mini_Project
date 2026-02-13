import asyncio
from models.manager import TaskManager
from utils.reminder import reminder_loop
from utils.date_util import validate_date, now_ist

YELLOW = "\033[1;33m"
RESET = "\033[0m"

# Prints UI header
def header():
    print(YELLOW + "\n" + "=" * 18 + " TASK MANAGER " + "=" * 18 + RESET)

# Displays menu options
def menu():
    print(YELLOW + " [1] Add Task      [2] Update Task" + RESET)
    print(YELLOW + " [3] Delete Task   [4] View All" + RESET)
    print(YELLOW + " [5] Mark Complete [6] Exit" + RESET)

# Main application loop
async def main():
    manager = TaskManager()
    asyncio.create_task(reminder_loop(manager))

    while True:
        header()
        menu()

        choice = await asyncio.to_thread(input, YELLOW + "Choice: " + RESET)

        if choice == "1":
            title = input(YELLOW + "Title: " + RESET)
            desc = input(YELLOW + "Description: " + RESET)

            while True:
                due_raw = input(YELLOW + "Due Date (YYYY-MM-DD HH:MM): " + RESET)
                date_obj, error = validate_date(due_raw)
                if date_obj:
                    due = due_raw
                    break
                print(YELLOW + error + RESET)

            start = now_ist().strftime("%Y-%m-%d %H:%M")
            manager.add_task(title, desc, start, due)

        elif choice == "2":
            try:
                tid = int(input(YELLOW + "Task ID: " + RESET))
                new_title = input(YELLOW + "New Title: " + RESET)
                new_status = input(YELLOW + "New Status: " + RESET)
                manager.update_task(tid, title=new_title or None, status=new_status or None)
            except ValueError:
                print(YELLOW + "Invalid numeric ID" + RESET)

        elif choice == "3":
            try:
                tid = int(input(YELLOW + "Task ID to delete: " + RESET))
                manager.delete_task(tid)
            except ValueError:
                print(YELLOW + "Invalid ID" + RESET)

        elif choice == "4":
            manager.view_tasks()

        elif choice == "5":
            try:
                tid = int(input(YELLOW + "Task ID to mark completed: " + RESET))
                manager.mark_completed(tid)
            except ValueError:
                print(YELLOW + "Invalid ID" + RESET)

        elif choice == "6":
            print(YELLOW + "Exiting Task Manager" + RESET)
            break

        else:
            print(YELLOW + "Invalid choice" + RESET)

if __name__ == "__main__":
    asyncio.run(main())
