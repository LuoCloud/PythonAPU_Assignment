import os
from datetime import datetime

LOG_FILE = "activity.log"

# Citation: Timestamp formatting using datetime.strftime referenced from Python Software Foundation (2024)
def log_action(action_type, details):
    # Get current date and time for auditing: YYYY-MM-DD HH:MM:SS
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{current_time}] [{action_type.upper()}] {details}\n"

    # Append the log message to activity.log
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_message)
    except Exception as err:
        print(f"Failed to record log: {err}")

def view_logs():
    # Check if the log file exists before opening
    if not os.path.exists(LOG_FILE):
        print("No audit log records found.")
        return

    print("\n --- System Audit Log ---")
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            for line in file:
                print(line.strip())
    except Exception as err:
        print(f"Failed to read audit log: {err}")