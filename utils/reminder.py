import asyncio
from datetime import datetime
from utils.date_util import now_ist, IST

# Background loop that shows upcoming tasks
async def reminder_loop(manager):
    while True:
        await asyncio.sleep(10)
        now = now_ist()
        pending = []

        for task in manager.tasks.values():
            if task.status.lower() == "completed":
                continue
            try:
                due = datetime.strptime(
                    task.due_date,
                    "%Y-%m-%d %H:%M"
                ).replace(tzinfo=IST)

                if due >= now:
                    pending.append(task)
            except:
                continue

        pending.sort(key=lambda t: datetime.strptime(t.due_date,"%Y-%m-%d %H:%M")
                     .replace(tzinfo=IST))

        if pending:
            print("\r\033[K\n" + "=" * 40)
            print("URGENT REMINDERS")
            print("-" * 40)

            for task in pending[:3]:
                print(f"{task.id} | {task.due_date} -> {task.title}")

            print("=" * 40)
            print("Choice: ", end="", flush=True)
