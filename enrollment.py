import os
from datetime import datetime
from audit_logger import log_action, view_logs
from login import is_admin

# File paths for data storage
ENROLLMENT_FILE = "enrollment.txt"
MEMBERS_FILE = "members.txt"
COURSES_FILE = "cmstorage.txt"

# Citation: File reading and string parsing adapted from W3Schools (2024)
def check_member_exists(member_id):
    # Verify if member ID exists in members.txt
    if not os.path.exists(MEMBERS_FILE):
        return False
    try:
        with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if not parts:
                    continue
                # Skip header row safely
                first_col = parts[0].strip().upper()
                if first_col in ["MEMBERID", "MEMBER_ID", "ID"]:
                    continue
                # Compare member ID
                if first_col == member_id.strip().upper():
                    return True
    except Exception:
        return False
    return False


def check_course_exists(course_id):
    # Verify if course ID exists in cmstorage.txt or courses.txt
    for course_file in [COURSES_FILE, "courses.txt"]:
        if os.path.exists(course_file):
            try:
                with open(course_file, "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("|")
                        if not parts:
                            continue
                        first_col = parts[0].strip().upper()
                        if first_col in ["COURSEID", "COURSE_ID", "ID"]:
                            continue
                        if first_col == course_id.strip().upper():
                            return True
            except Exception:
                pass
    return False


def load_all_enrollments():
    # Read all records from enrollments.txt, skipping header if present
    records = []
    if not os.path.exists(ENROLLMENT_FILE):
        return records
    try:
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                clean_line = line.strip()
                if clean_line:
                    parts = clean_line.split("|")
                    # Skip header line safely
                    if parts[0].strip().upper() in ["ENROLLMENTID", "ENROLLMENT_ID", "ID"]:
                        continue
                    records.append(parts)
    except Exception:
        pass
    return records


def generate_enrollment_id(records):
    # Scan existing IDs to find highest number to prevent duplicates after deletion
    max_id = 0
    for row in records:
        rec_id = row[0].strip().upper()
        if rec_id.startswith("E") and rec_id[1:].isdigit():
            curr_num = int(rec_id[1:])
            if curr_num > max_id:
                max_id = curr_num
    next_id = max_id + 1
    return f"E{next_id:03d}"


def create_enrollment():
    print("\n--- Enroll Member into Course ---")
    member_id = input("Enter Member ID: ").strip()
    if not check_member_exists(member_id):
        print("Error: Member ID not found in members.txt!")
        return

    course_id = input("Enter Course ID: ").strip()
    if not check_course_exists(course_id):
        print("Error: Course ID not found in course storage!")
        return

    records = load_all_enrollments()
    new_id = generate_enrollment_id(records)
    enroll_date = datetime.now().strftime("%Y-%m-%d")
    status = "Active"

    # Save new record using pipe delimiter
    try:
        with open(ENROLLMENT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{new_id}|{member_id}|{course_id}|{enroll_date}|{status}\n")
        print(f"Success: Enrollment recorded! Assigned ID: {new_id}")
        log_action("ENROLL", f"Created enrollment {new_id} for member {member_id} in course {course_id}")
    except Exception as err:
        print(f"Error saving enrollment: {err}")


def read_enrollments():
    print("\n --- View Enrollment Records ---")
    records = load_all_enrollments()
    if not records:
        print("No enrollment records available.")
        return

    print("1. View All Records")
    print("2. Search by Member ID")
    print("3. Search by Course ID")
    sub_choice = input("Enter choice (1-3): ").strip()

    filtered_results = []
    if sub_choice == "1":
        filtered_results = records
    elif sub_choice == "2":
        search_mid = input("Enter Member ID: ").strip().upper()
        for row in records:
            if row[1].strip().upper() == search_mid:
                filtered_results.append(row)
    elif sub_choice == "3":
        search_cid = input("Enter Course ID: ").strip().upper()
        for row in records:
            if row[2].strip().upper() == search_cid:
                filtered_results.append(row)
    else:
        print("Invalid choice.")
        return

    if not filtered_results:
        print("No matching enrollment records found.")
        return

    # Formatted table output
    print("\n" + "=" * 65)
    print(f"{'Enroll ID':<12} {'Member ID':<12} {'Course ID':<12} {'Date':<14} {'Status':<10}")
    print("=" * 65)
    for r in filtered_results:
        print(f"{r[0]:<12} {r[1]:<12} {r[2]:<12} {r[3]:<14} {r[4]:<10}")
    print("=" * 65)


def update_enrollment():
    print("\n--- Update Enrollment Status ---")
    target_id = input("Enter Enrollment ID to update: ").strip().upper()
    records = load_all_enrollments()
    found = False
    new_status = ""

    for row in records:
        if row[0].strip().upper() == target_id:
            found = True
            print(f"Current Status: {row[4]}")
            print("Select new status:")
            print("1. Active")
            print("2. Completed")
            print("3. Withdrawn")
            stat_choice = input("Enter option (1-3): ").strip()

            if stat_choice == "1":
                new_status = ("Active")
            elif stat_choice == "2":
                new_status = ("Completed")
            elif stat_choice == "3":
                new_status = ("Withdrawn")
            else:
                print("Invalid status selection.")
                return

            row[4] = new_status
            break

    if not found:
        print("Error: Enrollment ID not found.")
        return

    # Rewrite updated list to file
    try:
        with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
            for row in records:
                f.write("|".join(row) + "\n")
        print("Status updated successfully.")
        log_action("UPDATE", f"Updated enrollment {target_id} status to {new_status}")
    except Exception as err:
        print(f"Failed to update file: {err}")


# Citation: List manipulation and file rewrite logic referenced from GeeksforGeeks (2025)
def delete_enrollment():
    print("\n--- Delete / Cancel Enrollment ---")
    target_id = input("Enter Enrollment ID to delete: ").strip().upper()
    records = load_all_enrollments()

    target_index = -1
    for i in range(len(records)):
        if records[i][0].strip().upper() == target_id:
            target_index = i
            break

    if target_index == -1:
        print("Error: Enrollment ID not found.")
        return

    confirm = input(f"Are you sure you want to delete {target_id}? (y/n): ").strip().lower()
    if confirm == "y":
        records.pop(target_index)
        try:
            with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
                for row in records:
                    f.write("|".join(row) + "\n")
            print("Enrollment record deleted successfully.")
            log_action("DELETE", f"Removed enrollment record {target_id}")
        except Exception as err:
            print(f"Failed to delete file: {err}")
    else:
        print("Deletion cancelled.")


def enrollment_menu(username=""):
    if is_admin(username):
        while True:
            print("\n=================================")
            print("  Enrollment Management (Admin)  ")
            print("=================================")
            print("1. Enroll Member into Course")
            print("2. View / Search Enrollments")
            print("3. Update Enrollment Status")
            print("4. Delete Enrollment Record")
            print("5. View Audit Logs (Feature)")
            print("6. Return to Main Menu")
            print("=================================")

            choice = input("Enter option (1-6): ").strip()
            if choice == "1":
                create_enrollment()
            elif choice == "2":
                read_enrollments()
            elif choice == "3":
                update_enrollment()
            elif choice == "4":
                delete_enrollment()
            elif choice == "5":
                view_logs()
            elif choice == "6":
                print("Returning to main system...")
                break
            else:
                print("Invalid input. Please choose 1 to 6.")
    else:
        while True:
            print("\n=================================")
            print("   Enrollment Menu (User View)   ")
            print("=================================")
            print("1. View / Search Enrollments")
            print("2. Return to Main Menu")
            print("=================================")

            choice = input("Enter option (1-2): ").strip()
            if choice == "1":
                read_enrollments()
            elif choice == "2":
                print("Returning to main system...")
                break
            else:
                print("Invalid input. Please choose 1 or 2.")


# Alias so `from enrollment import enrollmentmenu` in main.py works seamlessly
def enrollmentmenu(username=""):
    enrollment_menu(username)
