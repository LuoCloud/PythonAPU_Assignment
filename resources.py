#!/usr/bin/python3
import os
import rr_filebackup
from login import is_admin

RESOURCE_FILE = "resources.txt"
ADMIN_FILE = "admins.txt"
FIELDS = ["Resource ID", "Name", "Type", "Quantity", "Status"]
MAX_RESOURCES = 20

# ---- THIS IS to read the whole file----
def openfile():
    print("\n---")
    if not os.path.exists(RESOURCE_FILE):
        print("No resources file found.")
        print("---\n")
        return
    with open(RESOURCE_FILE, "r") as file:
        content = file.read()
        print(content)
    print("---\n")


# ---- Check for users' access ---- #
admin_file = 'admins.txt'

def users_exists(username):
    return is_admin(username)


# ---- Helpers for main ---- #
def get(prompt, field):
    while True:
        value = input(prompt).strip()
        if "|" in value:
            print("'|' character is not allowed.")
        elif value == "":
            print(f"{field} cannot be empty.")
        elif field == "Quantity" and (not value.isdigit() or int(value) == 0):
            print("Quantity must be a whole number greater than 0.")
        else:
            return value.upper()

def load():
    records = []
    try:
        with open(RESOURCE_FILE, "r") as file:
            for line in file:
                line = line.strip().strip("|")
                if line:
                    parts = line.split("|")
                    for i in range(len(parts)):
                        parts[i] = parts[i].strip()
                    if len(parts) != len(FIELDS):
                        print("Skipped a line with wrong format:", line)
                        continue
                    records.append(parts)
    except FileNotFoundError:
        pass
    finally:
        print("Loading completed!")
    return records

def save(records):
    rr_filebackup.save(RESOURCE_FILE)
    with open(RESOURCE_FILE, "w") as file:
        for record in records:
            file.write("|".join(record) + "\n")

def find(records, rcid):
    for record in records:
        rcid = rcid.strip().lower()
        if record[0].lower() == rcid:
            return record
    return None

def confirm(message):
    answer = input(message + " (Y / N): ").strip().lower()
    while answer not in ("y", "Y", "yes", "YES", "Yes", "n", "N", "no", "NO", "No"):
        answer = input("Please enter yes or no: ").strip().lower()
    return answer in ("y", "Y", "yes", "YES", "Yes")

def show_tables(records):
    if not records:
        print("No resources found.")
        return
    print(f"{'ID':<8}{'Name':<20}{'Type':<15}{'Qty':<6}{'Status':<12}")
    print("-" * 61)
    for record in records:
        print(f"{record[0]:<8}{record[1]:<20}{record[2]:<15}{record[3]:<6}{record[4]:<12}")

def is_full(records):
    if len(records) >= MAX_RESOURCES:
        print("Resources Max")
        return True
    return False

def undo_change():
    if rr_filebackup.undo(RESOURCE_FILE):
        print("Last change undone.")
    else:
        print("Nothing to undo.")

def back(username):
    print("\nLoading...")
    print("---")
    print("Back to Resource Menu.")
    resourcemenu(username)

def get_status(prompt):
    status = get(prompt, "Status")
    while status not in ("AVAILABLE", "UNAVAILABLE"):
        print("Format Error. Please type Available / Unavailable.")
        status = get(prompt, "Status")
    return status

# ---- Filter by more than one field ---- #
def filtering(username):
    options = ["Members", "Courses", "Enrollments", "Resources"]
    while True:
        print("\n----! FILTER !----")
        print("Which data do you want to filter?")
        for i in range(len(options)):
            print(f" {i + 1}. {options[i]}")
        choice = input("Number (b to go back): ").strip()
        if choice in ("b", "B"):
            return
        if not choice.isdigit() or not 1 <= int(choice) <= len(options):
            print("Invalid choice.")
        elif options[int(choice) - 1] == "Resources":
            filter_resources()
        else:
            print(f"{options[int(choice) - 1]} filter is not available yet.")

def filter_resources():
    records = load()
    print("Please enter...")
    choice = input("(c)ontinue, (b)ack: ")
    while choice not in ("b", "B"):
        if choice in ("c", "C"):
            print("Which fields do you want to filter by? (e.g. 3,5 for Type + Status)")
            for i in range(len(FIELDS)):
                print(f" {i + 1}. {FIELDS[i]}")
            raw = input("Numbers separated by commas: ").strip()

            picks = []
            valid = True
            for part in raw.split(","):
                part = part.strip()
                if part.isdigit() and 1 <= int(part) <= len(FIELDS):
                    if FIELDS[int(part) - 1] not in picks:
                        picks.append(FIELDS[int(part) - 1])
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
                    conditions[field] = value

                results = []
                for record in records:
                    match = True
                    for field in conditions:
                        cell = record[FIELDS.index(field)].lower()
                        if field == "Quantity" or field == "Status":
                            if cell != conditions[field]:
                                match = False
                        elif conditions[field] not in cell:
                            match = False
                    if match:
                        results.append(record)

                show_tables(results)
                print(len(results), "result(s) found.")
        else:
            print("Invalid command.")
        choice = input("(c)ontinue, (b)ack: ")

# ---- Main Functions ---- #
# ---- Create ---- #
def create(username):
    records = load()
    print("Please enter...")
    choice = input("(c)ontinue, (b)ack: ")
    while choice not in ("q", "Q"):
        while choice not in ("c", "C", "q", "Q", "b", "B"):
            print("Invalid command.")
            choice = input("Please enter (c)ontinue / (b)ack: ")
        if choice in ("B", "b"):
            back(username)
            return
        elif choice in ("C", "c"):
            if is_full(records):
                return
            rcid = get("Resource ID: ", "Resource ID")
            while find(records, rcid) is not None:
                print("This ID already exists.")
                rcid = get("Resource ID: ", "Resource ID")
            name = get("Resource Name: ", "Resource Name")
            rtype = get("Category: ", "Category")
            qty = get("Quantity: ", "Quantity")
            status = get_status("Status (Available / Unavailable): ")
            records.append([rcid, name, rtype, qty, status])
            save(records)
            print("Resource added!")
            choice = input("(c)ontinue, (b)ack: ")
    exit

# ---- Read ---- #
def read(username):
    records = load()
    print("Please enter...")
    choice = input("(a)ll, (s)earch by ID/name/type, (f)ilter, (b)ack: ")
    while choice not in ("q", "Q"):
        while choice not in ("a", "A", "s", "S", "b", "B", "f", "F"):
            choice = input("Please enter (a)ll / (s)earch / (f)ilter / (b)ack: ")
        if choice in ("a", "A"):
            openfile()
        elif choice in ("b", "B"):
            back(username)
            return
        elif choice in ("f", "F"):
            filtering(username)
            back(username)
            return
        elif choice in ("s", "S"):
            keyword = input("Search for: ").strip().lower()
            if keyword == "b":
                back(username)
                return
            matches = []
            for line in records:
                if keyword in line[0].lower() or keyword in line[1].lower() or keyword in line[2].lower():
                    matches.append(line)
            show_tables(matches)
        choice = input("(a)ll, (s)earch by ID/name/type, (f)ilter, (b)ack: ")
    exit

# ---- Edit ---- #
def update(username):
    records = load()
    choice = input("(c)ontinue, (b)ack: ")
    while choice not in ("q", "Q"):
        while choice not in ("c", "C", "q", "Q", "b", "B"):
            print("Invalid input.")
            choice = input("Please enter (c)ontinue, (b)ack")
        if choice in ("b", "B"):
            back(username)
            return
        if choice in ("c", "C"):
            rcid = input("Resource ID to edit: ").strip()
            record = find(records, rcid)
            while record is None:
                print("ID not found.")
                rcid = input("Enter existing Resource ID: ").strip()
                print("PRESS 'Q' to cancel.")
                if rcid in ("q", "Q"):
                    return
                record = find(records, rcid)
            print("Which field do you want to change?")
            for i in range(len(FIELDS)):
                print(f" {i + 1}. {FIELDS[i]} (now: {record[i]}) ")
            pick = input("Number: ").strip()
            if not pick.isdigit() or not 1 <= int(pick) <= len(FIELDS):
                print("Invalid choice.")
                return
            index = int(pick) - 1
            if pick == "5":
                new_value = get_status("New Status (Available / Unavailable): ")
            else:
                new_value = get(f"New {FIELDS[index]}: ", FIELDS[index])
            if index == 0 and find(records, new_value) is not None:
                print("That ID already exists. Nothing changed.")
                return
            record[index] = new_value
            save(records)
            print("Updated.")
        return
    exit

# ---- Delete ---- #
def delete(username):
    records = load()
    print("Please enter...")
    choice = input("(c)ontinue, (b)ack: ")
    while choice not in ("q", "Q"):
        while choice not in ("c", "C", "q", "Q", "b", "B"):
            print("Invalid command.")
            choice = input("Please enter (c)ontinue / (b)ack: ")
        if choice in ("b", "B"):
            back(username)
            return
        elif choice in ("c", "C"):
            rcid = input("Resource ID to delete: ").strip()
            record = find(records, rcid)
            while record is None:
                print("ID not found.")
                rcid = input("Enter existing Resource ID: ").strip()
                record = find(records, rcid)
                print("PRESS 'Q' to exit.")
                if rcid in ("q", "Q"):
                    return
            if confirm(f"Delete {record[1]} ({record[0]})?"):
                records.remove(record)
                save(records)
                print("Deleted.")
            else:
                print("Cancelled.")
    exit


# ---- Main menu for resources ---- #
def resourcemenu(username):
    print("\nPRESS 'Q' to quit program.")
    print("----! RESOURCE MENU !----")
    print("| ID | NAME | CATEGORY | QUANTITY | STATUS |\n")
    print(f"{username}, ")
    if is_admin(username) == False:
        print(f"you don't have access to edit.\n")
        choice = input("Do you want to continue? (Y / N): ")
        while choice not in ("n", "N", "No", "no", "NO", "q", "Q"):
            print("Command accepted.")
            choice = input("(r)ead, (q)uit: ")
            if choice in ("r", "R"):
                read(username)
                break
            else:
                print("Program executed.")
                return
    else:
        print("access granted!\n")
        print("Please enter...")
        choice = input("(c)reate, (r)ead, (u)pdate, (d)elete, (q)uit : ")
        print("---\nEntered.")
        while choice not in ("q", "Q"):
            while choice not in ("r", "R", "u", "U", "d", "D", "c", "C", "q", "Q"):
                print("Invalid.")
                choice = input("Please enter (c)reate, (r)ead, (u)pdate, (d)elete, (q)uit : ")
            if choice in ("c", "C"):
                create(username)
                break
            if choice in ("r", "R"):
                read(username)
                break
            if choice in ("u", "U"):
                update(username)
                break
            if choice in ("d", "D"):
                delete(username)
                break
    print("Program executed.(Resource)")
