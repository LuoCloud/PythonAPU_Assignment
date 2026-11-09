# Shared functions for the Community Learning Hub system
from pathlib import Path
import hashlib
import os
import hmac

MEMBER_FILE = "members.txt"
STUDENT_FILE = "student_accounts.txt"
ADMIN_FILE = "admins.txt"
SEPARATOR = "|"
MIN_AGE = 18
MAX_AGE = 50

MEMBER_HEADER = "MemberID|Name|Age|Gender|ContactNumber|Email|StartDate\n"
GENDER_OPTIONS = {"1": "Male", "2": "Female", "3": "Other"}
ACCOUNT_HEADER = "Username|Salt|PasswordHash\n"
LINK_FILE = "student_links.txt"
LINK_HEADER = "Username|MemberID\n"

# This section of code create data files with headers when they don't exist.
def initialise_files():
    if not Path(MEMBER_FILE).exists():
        Path(MEMBER_FILE).write_text(MEMBER_HEADER, encoding="utf-8")
    if not Path(STUDENT_FILE).exists():
        Path(STUDENT_FILE).write_text(ACCOUNT_HEADER, encoding="utf-8")
    if not Path(ADMIN_FILE).exists():
        Path(ADMIN_FILE).write_text(ACCOUNT_HEADER, encoding="utf-8")
    if not Path(LINK_FILE).exists():
        Path(LINK_FILE).write_text(LINK_HEADER, encoding="utf-8")

# This section of code read valid pipe-separated rows, skipping malformed rows.
def read_rows(filename, expected_fields):
    rows = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            next(file, None)  # Skip the header.
            for line in file:
                line = line.strip()
                if not line:
                    continue
                fields = line.split(SEPARATOR)
                if len(fields) == expected_fields:
                    rows.append(fields)
    except FileNotFoundError:
        print(f"Data file '{filename}' was not found.")
    except OSError as error:
        print(f"Unable to read '{filename}': {error}")
    return rows

# This section of code rewrite a data file.
def write_rows(filename, header, rows):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(header)
            for row in rows:
                file.write(SEPARATOR.join(str(value) for value in row) + "\n")
        return True
    except OSError as error:
        print(f"Unable to save data: {error}")
        return False

def read_members():
    return read_rows(MEMBER_FILE, 7)

def save_members(members):
    return write_rows(MEMBER_FILE, MEMBER_HEADER, members)

# This section of code generate the next ID from the highest existing M-number.
def generate_member_id(members):
    highest = 0
    for member in members:
        try:
            number = int(member[0][1:])
            if number > highest:
                highest = number
        except (ValueError, IndexError):
            continue
    return f"M{highest + 1:04d}"

def get_non_empty(prompt, field_name):
    while True:
        value = input(prompt).strip()
        if not value:
            print(f"{field_name} cannot be empty.")
        elif SEPARATOR in value:
            print(f"{field_name} cannot contain the '|' character.")
        else:
            return value

def get_age():
    while True:
        value = input(f"Age ({MIN_AGE}-{MAX_AGE}): ").strip()
        try:
            age = int(value)
            if MIN_AGE <= age <= MAX_AGE:
                return str(age)
            print(f"Age must be between {MIN_AGE} and {MAX_AGE}.")
        except ValueError:
            print("Please enter a whole number.")

def get_contact():
    while True:
        contact = input("Contact number: ").strip()
        digits = contact[1:] if contact.startswith("+") else contact
        if digits.isdigit() and 7 <= len(digits) <= 15:
            return contact
        print("Enter 7-15 digits; an optional leading + is allowed.")

# This section of code ask for gender using a numbered menu so spelling errors are impossible.
def get_gender():
    while True:
        print("Gender:")
        for number, label in GENDER_OPTIONS.items():
            print(f"  {number}. {label}")
        choice = input("Choose 1-3: ").strip()
        if choice in GENDER_OPTIONS:
            return GENDER_OPTIONS[choice]
        print("Please choose 1, 2 or 3.")

# This section of code ask for a student username that is not already taken.
def get_unique_student_username():
    while True:
        username = get_non_empty("Choose a username: ", "Username")
        if any(row[0].lower() == username.lower()
               for row in read_accounts(STUDENT_FILE)):
            print("That username is already taken.")
        else:
            return username

def get_email():
    while True:
        email = input("Email address: ").strip()
        if (email.count("@") == 1 and "." in email.split("@")[-1]
                and " " not in email and SEPARATOR not in email):
            return email
        print("Please enter a valid-looking email address.")

def collect_member_details():
    name = get_non_empty("Full name: ", "Name")
    age = get_age()
    gender = get_gender()
    contact = get_contact()
    email = get_email()
    return [name, age, gender, contact, email]

# This section of code hash a password using Python's standard-library PBKDF2 function.
def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), 200000
    ).hex()
    return salt, digest

def verify_password(password, salt, stored_hash):
    _, candidate_hash = hash_password(password, salt)
    return hmac.compare_digest(candidate_hash, stored_hash)

def get_new_password():
    while True:
        password = input("Create password (at least 8 characters): ")
        if len(password) < 8:
            print("Password must contain at least 8 characters.")
            continue
        confirm = input("Confirm password: ")
        if password == confirm:
            return password
        print("Passwords do not match.")

def read_accounts(filename):
    return read_rows(filename, 3)

def add_account(filename, username, password):
    accounts = read_accounts(filename)
    if any(account[0].lower() == username.lower() for account in accounts):
        print("That username is already in use.")
        return False
    salt, digest = hash_password(password)
    accounts.append([username, salt, digest])
    return write_rows(filename, ACCOUNT_HEADER, accounts)

# This section of code remove one account by username. Returns True only if it was saved.
def remove_account(filename, username):
    accounts = read_accounts(filename)
    remaining = [
        account for account in accounts
        if account[0].lower() != username.lower()
    ]
    if len(remaining) == len(accounts):
        return False  # Username not found.
    return write_rows(filename, ACCOUNT_HEADER, remaining)

def authenticate(filename, username, password):
    accounts = read_accounts(filename)
    for account in accounts:
        if account[0].lower() == username.lower():
            return verify_password(password, account[1], account[2])
    return False

def find_student_member_id(username, password):
    accounts = read_accounts(STUDENT_FILE)
    for account in accounts:
        if account[0].lower() == username.lower() and verify_password(
                password, account[1], account[2]):
            # Student usernames are linked to Member IDs in a separate mapping file.
            return get_student_member_link(username)
    return None

def get_student_member_link(username):
    links = read_rows(LINK_FILE, 2)
    for link in links:
        if link[0].lower() == username.lower():
            return link[1]
    return None

def add_student_account(username, password, member_id):
    if not add_account(STUDENT_FILE, username, password):
        return False
    links = read_rows(LINK_FILE, 2)
    links.append([username, member_id])
    if write_rows(LINK_FILE, LINK_HEADER, links):
        return True
    # Roll back the account so no orphan login remains.
    accounts = [
        account for account in read_accounts(STUDENT_FILE)
        if account[0].lower() != username.lower()
    ]
    write_rows(STUDENT_FILE, ACCOUNT_HEADER, accounts)
    return False

def get_member_by_id(members, member_id):
    for member in members:
        if member[0].lower() == member_id.lower():
            return member
    return None

def display_member(member):
    labels = ["Member ID", "Name", "Age", "Gender", "Contact Number", "Email", "Start Date"]
    print("\n--- Member Details ---")
    for index, label in enumerate(labels):
        print(f"{label}: {member[index]}")
    print("----------------------")

def print_member_table(members):
    if not members:
        print("No member records found.")
        return
    print("\n" + "-" * 110)
    print(f"{'ID':<8}{'Name':<24}{'Age':<6}{'Gender':<9}{'Contact':<18}{'Email':<32}{'Start Date'}")
    print("-" * 110)
    for member in members:
        print(f"{member[0]:<8}{member[1][:22]:<24}{member[2]:<6}{member[3]:<9}"
              f"{member[4][:16]:<18}{member[5][:30]:<32}{member[6]}")
    print("-" * 110)