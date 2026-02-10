import asyncio
from datetime import datetime

async def reminder_loop(manager):
    """Prints urgent sorted tasks every 10s without breaking the UI."""
    while True:
        await asyncio.sleep(10)
        # Sort pending tasks by due date
        pending = [t for t in manager.tasks.values() if t.status.lower() != "completed"]
        pending.sort(key=lambda x: datetime.strptime(x.due_date, "%Y-%m-%d %H:%M"))

        if pending:
            # \r\033[K clears the current input line, \033[1;33m is Yellow Bold
            print(f"\r\033[K\n\033[1;33m{'='*40}\n🔔 URGENT REMINDERS(Sorted by Due Date)\n{'-'*40}")
            for t in pending[:3]: # Show top 3 most urgent
                print(f"{t.id} ⚠️ {t.due_date} -> {t.title}")
            print(f"{'='*40}\033[0m")
            print("Choice: ", end="", flush=True)
            