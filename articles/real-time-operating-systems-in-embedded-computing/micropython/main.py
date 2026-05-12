# MicroPython cooperative timing prototype.
# This is not a real RTOS. It sketches timing contracts for constrained boards.

import time

tasks = [
    {"name": "control_loop", "period_ms": 20, "deadline_ms": 20, "last_ms": 0},
    {"name": "sensor_acquisition", "period_ms": 50, "deadline_ms": 40, "last_ms": 0},
    {"name": "diagnostics", "period_ms": 1000, "deadline_ms": 800, "last_ms": 0},
]

def now_ms():
    return int(time.time() * 1000)

def run_task(task):
    start = now_ms()
    # Replace with real work.
    elapsed = now_ms() - start
    deadline_miss = elapsed > task["deadline_ms"]
    print({"task": task["name"], "elapsed_ms": elapsed, "deadline_miss": deadline_miss})

while True:
    current = now_ms()
    for task in tasks:
        if current - task["last_ms"] >= task["period_ms"]:
            run_task(task)
            task["last_ms"] = current
    time.sleep(0.001)
