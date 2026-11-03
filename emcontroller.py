# main logic for handling enrollment operations

import os
import json
from datetime import datetime
from emconfig import ENROLLMENT_FILE, MEMBER_FILE, COURSE_JSON_FILE
from emview import show_menu, display_table, status_menu

def check_member_exists(member_id):
    # check if this member id is actually in members.txt
    if not os.path.exists(MEMBER_FILE):
        return False
    try:
        with open(MEMBER_FILE, "r", encoding="utf-8") as f:
            next(f)
            for line in f:
                parts = line.strip().split("|")
                if parts and parts[0].strip().upper() == member_id.strip().upper():
                    return True
    except Exception:
        pass
    return False

def check_course_exists(course_id):
    # check if course exists in json storage
    if not os.path.exists(COURSE_JSON_FILE):
        return False
    try:
        with open(COURSE_JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for key in data:
                if key.strip().upper() == course_id.strip().upper():
                    return True
    except Exception:
        pass
    return False

def load_all_enrollments():
    # helper to grab all current records from file
    records = []
    if not os.path.exists(ENROLLMENT_FILE):
        return records
    try:
        with open(ENROLLMENT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    records.append(line.strip().split(","))
    except Exception:
        pass
    return records

def generate_enrollment_id(records):
    # scan existing records to find the highest number and prevent duplication after deletion
    max_num = 0
    for r in records:
        if r[0].startswith("E") and r[0][1:].isdigit():
            num = int(r[0][1:])
            if num > max_num:
                max_num = num
    return f"E{max_num + 1:03d}"

def create_enrollment():
    # create a new enrollment entry
    print("\nadd enrollment process")
    member_id = input("input member id: ").strip()
    if not check_member_exists(member_id):
        print("member id not found.")
        return

    course_id = input("input course id: ").strip()
    if not check_course_exists(course_id):
        print("course id not found.")
        return

    records = load_all_enrollments()
    new_id = generate_enrollment_id(records)
    date_str = datetime.now().strftime("%Y-%m-%d")
    status = "Active"

    try:
        with open(ENROLLMENT_FILE, "a", encoding="utf-8") as f:
            f.write(f"{new_id},{member_id},{course_id},{date_str},{status}\n")
        print(f"saved successfully. id is {new_id}")
    except Exception as e:
        print(f"write failed: {e}")

def read_enrollments():
    # view or filter existing records
    print("\nview enrollments")
    records = load_all_enrollments()
    if not records:
        print("no records found.")
        return

    print("1. view all")
    print("2. search by member id")
    print("3. search by course id")
    choice = input("choose: ").strip()

    target = records
    if choice == "2":
        m_id = input("member id: ").strip()
        target = [r for r in records if r[1].upper() == m_id.upper()]
    elif choice == "3":
        c_id = input("course id: ").strip()
        target = [r for r in records if r[2].upper() == c_id.upper()]

    display_table(target)

def update_enrollment():
    # update status of an enrollment with case-insensitive id check
    print("\nupdate enrollment status")
    e_id = input("target enrollment id: ").strip().upper()
    records = load_all_enrollments()
    found = False
    updated = []

    for r in records:
        if r[0].upper() == e_id:
            found = True
            print(f"current: {r[4]}")
            status_menu()
            sub = input("choice: ").strip()
            if sub == "1":
                r[4] = "Active"
            elif sub == "2":
                r[4] = "Completed"
            elif sub == "3":
                r[4] = "Withdrawn"
            print("status updated.")
        updated.append(r)

    if found:
        try:
            with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
                for r in updated:
                    f.write(",".join(r) + "\n")
        except Exception as e:
            print(f"update failed: {e}")
    else:
        print("id not found.")

def delete_enrollment():
    # remove an enrollment record with case-insensitive id check
    print("\ndelete enrollment")
    e_id = input("target enrollment id: ").strip().upper()
    records = load_all_enrollments()
    found = False
    updated = []

    for r in records:
        if r[0].upper() == e_id:
            found = True
        else:
            updated.append(r)

    if found:
        confirm = input("are you sure? y/n: ").strip().lower()
        if confirm == 'y':
            try:
                with open(ENROLLMENT_FILE, "w", encoding="utf-8") as f:
                    for r in updated:
                        f.write(",".join(r) + "\n")
                print("deleted.")
            except Exception as e:
                print(f"delete failed: {e}")
        else:
            print("cancelled.")
    else:
        print("id not found.")

def enrollment_menu():
    # main loop for enrollment
    while True:
        show_menu()
        choice = input("select: ").strip()
        if choice == "1":
            create_enrollment()
        elif choice == "2":
            read_enrollments()
        elif choice == "3":
            update_enrollment()
        elif choice == "4":
            delete_enrollment()
        elif choice == "5":
            break

if __name__ == "__main__":
    enrollment_menu()