# MicroPython watchdog-like heartbeat and diagnostic prototype.
# Replace simulated checks with board-specific watchdog and health APIs.

import time

fault_counter = 0
watchdog_reset_counter = 0

def critical_task_heartbeat():
    return True

def state_valid():
    return True

def queue_below_threshold():
    return False

def may_feed_watchdog():
    return critical_task_heartbeat() and state_valid() and queue_below_threshold()

while True:
    if may_feed_watchdog():
        print({"watchdog": "feed", "health": "normal"})
    else:
        fault_counter += 1
        print({"watchdog": "do_not_feed", "health": "degraded", "fault_counter": fault_counter})
    time.sleep(1)
