import asyncio


async def reminder_loop(tasks_list):
    """Prints urgent sorted tasks every 10s without breaking the UI."""
    while True:
        await asyncio.sleep(10)

        if tasks_list:
            sorted_tasks = sorted(tasks_list, key=lambda x: str(x[2]))

            print(f"\r\033[K\n\033[1;33m{'='*40}")
            print(f"🔔 URGENT REMINDERS (Sorted by Due Date)\n{'-'*40}")

            for t in sorted_tasks[:3]:
                if t[3] != 'Completed':    
                    print(
                        f"{t[0]} -> ⚠️ {t[2]} ------ {t[1]}"
                    )

            print(f"{'='*40}\033[0m")
            print("Choice: ", end="", flush=True)
