#!/usr/bin/python3
import os
from login import is_admin

# ---- Field names and column widths for each module ---- #
MEMBER_FIELDS = ["Member ID", "Name", "Age", "Gender", "Contact Number", "Email", "Start Date"]
MEMBER_WIDTHS = [10, 22, 6, 9, 16, 28, 12]
MEMBER_EXACT = ["Age", "Gender"]

COURSE_FIELDS = ["Course ID", "Course Name", "Instructor", "Duration", "Fee", "Capacity"]
COURSE_WIDTHS = [14, 26, 20, 14, 12, 10]
COURSE_EXACT = ["Capacity"]

ENROLLMENT_FIELDS = ["Enroll ID", "Member ID", "Course ID", "Enroll Date", "Status"]
ENROLLMENT_WIDTHS = [12, 12, 14, 14, 12]
ENROLLMENT_EXACT = ["Status"]

RESOURCE_FIELDS = ["Resource ID", "Name", "Type", "Quantity", "Status"]
RESOURCE_WIDTHS = [12, 22, 16, 10, 14]
RESOURCE_EXACT = ["Quantity", "Status"]


# ---- Load data from each module's file ---- #
def load_members():
    import member
    member.initialise_files()
    return member.read_members()


def load_courses():
    from cmdatabase import load_coursedata
    coursedata = load_coursedata()
    records = []
    for cid in coursedata:
        details = coursedata[cid]
        row = [
            str(cid),
            str(details["courname"]),
            str(details["courinstructor"]),
            str(details["courduration"]),
            str(details["courfee"]),
            str(details["courcapacity"]),
        ]
        records.append(row)
    return records


def load_enrollments():
    import enrollment
    return enrollment.load_all_enrollments()


def load_resources():
    records = []
    if not os.path.exists("resources.txt"):
        return records
    try:
        with open("resources.txt", "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip().strip("|")
                if line:
                    parts = line.split("|")
                    for i in range(len(parts)):
                        parts[i] = parts[i].strip()
                    if len(parts) == len(RESOURCE_FIELDS):
                        records.append(parts)
    except FileNotFoundError:
        pass
    return records


# ---- Display results in a neat table ---- #
def show_table(records, fields, widths):
    if not records:
        print("No matching records found.")
        return

    line_length = 0
    header = ""
    for i in range(len(fields)):
        header = header + f"{fields[i]:<{widths[i]}} "
        line_length = line_length + widths[i] + 1

    print()
    print("-" * line_length)
    print(header)
    print("-" * line_length)

    for record in records:
        row_text = ""
        for i in range(len(fields)):
            value = str(record[i]) if i < len(record) else ""
            if len(value) > widths[i]:
                value = value[: widths[i] - 2] + ".."
            row_text = row_text + f"{value:<{widths[i]}} "
        print(row_text)
    print("-" * line_length)


# ---- Keyword search across all fields ---- #
def run_search(records, fields, widths, title):
    print(f"\n--- Search {title} ---")
    choice = input("(c)ontinue, (b)ack: ").strip()
    while choice not in ("b", "B"):
        if choice in ("c", "C"):
            if not records:
                print(f"No {title.lower()} found.")
                return
            keyword = input("Search for (b to cancel): ").strip().lower()
            if keyword == "b":
                return
            if keyword == "":
                print("Search keyword cannot be empty.")
            else:
                matches = []
                for record in records:
                    found = False
                    for cell in record:
                        if keyword in str(cell).lower():
                            found = True
                    if found:
                        matches.append(record)
                show_table(matches, fields, widths)
                print(len(matches), "result(s) found.")
        else:
            print("Invalid command.")
        choice = input("(c)ontinue, (b)ack: ").strip()


# ---- Filter by one or more fields ---- #
def run_filter(records, fields, exact_fields, widths, title):
    print(f"\n--- Filter {title} ---")
    choice = input("(c)ontinue, (b)ack: ").strip()
    while choice not in ("b", "B"):
        if choice in ("c", "C"):
            if not records:
                print(f"No {title.lower()} found.")
                return

            print("Which fields do you want to filter by? (e.g. 1,3 for multiple fields)")
            for i in range(len(fields)):
                print(f" {i + 1}. {fields[i]}")
            raw = input("Numbers separated by commas: ").strip()

            picks = []
            valid = True
            for part in raw.split(","):
                part = part.strip()
                if part.isdigit() and 1 <= int(part) <= len(fields):
                    field_name = fields[int(part) - 1]
                    if field_name not in picks:
                        picks.append(field_name)
                else:
                    valid = False

            if not valid or len(picks) == 0:
                print("Invalid choice.")
            else:
                conditions = {}
                for field in picks:
                    value = ""
                    while value == "":
                        value = input(f"{field}: ").strip().lower()
                        if value == "":
                            print(f"{field} cannot be empty.")
                    conditions[field] = value

                results = []
                for record in records:
                    match = True
                    for field in conditions:
                        idx = fields.index(field)
                        cell = str(record[idx]).strip().lower()
                        if field in exact_fields:
                            if cell != conditions[field]:
                                match = False
                        else:
                            if conditions[field] not in cell:
                                match = False
                    if match:
                        results.append(record)

                show_table(results, fields, widths)
                print(len(results), "result(s) found.")
        else:
            print("Invalid command.")
        choice = input("(c)ontinue, (b)ack: ").strip()


# ---- Choose search or filter for a module ---- #
def search_or_filter(records, fields, exact_fields, widths, title):
    while True:
        print(f"\n---- {title}: Search & Filter ----")
        print("1. Keyword Search")
        print("2. Multi-Field Filter")
        print("3. Back")
        choice = input("Choose 1-3: ").strip()

        if choice == "1":
            run_search(records, fields, widths, title)
        elif choice == "2":
            run_filter(records, fields, exact_fields, widths, title)
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


# ---- Main filter menu called from main.py -> (o)ther -> (f)ilter ---- #
def filtering(username=""):
    options = ["Members", "Courses", "Enrollments", "Resources"]
    while True:
        print("\n----! FILTER !----")
        print("Which data do you want to search or filter?")
        for i in range(len(options)):
            if options[i] == "Members" and username != "" and not is_admin(username):
                print(f" {i + 1}. {options[i]} (Admin only)")
            else:
                print(f" {i + 1}. {options[i]}")
        choice = input("Number (b to go back): ").strip()

        if choice in ("b", "B"):
            return
        if not choice.isdigit() or not 1 <= int(choice) <= len(options):
            print("Invalid choice.")
        elif options[int(choice) - 1] == "Members":
            if username != "" and not is_admin(username):
                print("Access denied: Only administrators can search or filter all members.")
            else:
                records = load_members()
                search_or_filter(records, MEMBER_FIELDS, MEMBER_EXACT, MEMBER_WIDTHS, "Members")
        elif options[int(choice) - 1] == "Courses":
            records = load_courses()
            search_or_filter(records, COURSE_FIELDS, COURSE_EXACT, COURSE_WIDTHS, "Courses")
        elif options[int(choice) - 1] == "Enrollments":
            records = load_enrollments()
            search_or_filter(records, ENROLLMENT_FIELDS, ENROLLMENT_EXACT, ENROLLMENT_WIDTHS, "Enrollments")
        elif options[int(choice) - 1] == "Resources":
            records = load_resources()
            search_or_filter(records, RESOURCE_FIELDS, RESOURCE_EXACT, RESOURCE_WIDTHS, "Resources")
