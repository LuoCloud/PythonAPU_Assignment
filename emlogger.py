# handle simple text-file log for auditing daily operations

import os
from datetime import datetime

LOG_FILE = "activity.log"

def log_action(action_type, details):
    """
    write a log entry into activity.log with timestamp for auditing.
    format: [YYYY-MM-DD HH:MM:SS] [ACTION_TYPE] Details
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{action_type.upper()}] {details}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"logging failed: {e}")

def view_logs():
    """
    view recorded activity logs for auditing purpose.
    """
    if not os.path.exists(LOG_FILE):
        print("no log records found")
        return

    print("\n--- system auditing logs ---")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            for line in f:
                print(line.strip())
    except Exception as e:
        print(f"read logs failed: {e}")
