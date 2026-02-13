import asyncio
from datetime import datetime


async def reminder_loop(manager):
    while True:
        try:
            await asyncio.sleep(10)

            tasks = manager.get_all_tasks()
            now = datetime.now()

            for t in tasks:
                if t['status'].lower() != "completed":
                    if t['due_date'] < now:
                        print(f"\n✅ Auto-completed Task {t['id']}")
                        manager.mark_completed(t['id'])

            pending = [
                t for t in manager.get_all_tasks()
                if t['status'].lower() != "completed"
            ]

            pending.sort(key=lambda x: x['due_date'])

            if pending:
                print("\n" + "="*40)
                print("🔔 URGENT REMINDERS")
                print("-"*40)
                for t in pending[:3]:
                    print(f"{t['id']} ⚠ {t['due_date']} -> {t['title']}")
                print("="*40)
                print("Choice: ", end="", flush=True)

        except Exception as e:
            print(f":x: Reminder error: {e}")