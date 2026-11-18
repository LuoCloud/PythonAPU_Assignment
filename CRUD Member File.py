# Community Learning Hub - Member Module
from datetime import date
from pathlib import Path
import hashlib
import hmac
import os


# Constants
MEMBER_FILE = "members.txt"
STUDENT_FILE = "student_accounts.txt"
ADMIN_FILE = "admins.txt"
LINK_FILE = "student_links.txt"
SEPARATOR = "|"
MIN_AGE = 18
MAX_AGE = 50

MEMBER_HEADER = "MemberID|Name|Age|Gender|ContactNumber|Email|StartDate\n"
ACCOUNT_HEADER = "Username|Salt|PasswordHash\n"
LINK_HEADER = "Username|MemberID\n"
GENDER_OPTIONS = {"1": "Male", "2": "Female", "3": "Other"}


# File handling
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


# Input validation
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

def get_contact():
    while True:
        contact = input("Contact number: ").strip()
        digits = contact[1:] if contact.startswith("+") else contact
        if digits.isdigit() and 7 <= len(digits) <= 15:
            return contact
        print("Enter 7-15 digits; an optional leading + is allowed.")

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


# Passwords and accounts
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

def authenticate(filename, username, password):
    accounts = read_accounts(filename)
    for account in accounts:
        if account[0].lower() == username.lower():
            return verify_password(password, account[1], account[2])
    return False

# This section of code ask for a student username that is not already taken.
def get_unique_student_username():
    while True:
        username = get_non_empty("Choose a username: ", "Username")
        if any(row[0].lower() == username.lower()
               for row in read_accounts(STUDENT_FILE)):
            print("That username is already taken.")
        else:
            return username

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


# Display helpers
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


# Student: register (Create) and login/view (Read)
# This section of code let a student register themselves and set their own password.
def student_register():
    print("\n=== Student Self-Registration ===")
    members = read_members()
    details = collect_member_details()
    username = get_unique_student_username()
    password = get_new_password()
    member_id = generate_member_id(members)
    member = [member_id] + details + [date.today().isoformat()]

    print("\nPlease review your details:")
    display_member(member)
    if input("Confirm registration? (Y/N): ").strip().lower() != "y":
        print("Registration cancelled.")
        return

    members.append(member)
    if not save_members(members):
        print("Registration was not completed because the member file could not be saved.")
        return

    if not add_student_account(username, password, member_id):
        # Roll back the member record if account creation fails.
        members.pop()
        save_members(members)
        print("Account creation failed. Registration was rolled back.")
        return

    print(f"Registration successful. Your Member ID is {member_id}.")
    print("Keep your username and password safe.")

# This section of code let a student log in and view only their own record.
def student_login():
    print("\n=== Student Login ===")
    username = input("Username: ").strip()
    password = input("Password: ")
    member_id = find_student_member_id(username, password)

    if member_id is None:
        print("Invalid username or password.")
        return

    member = get_member_by_id(read_members(), member_id)
    if member is None:
        print("Your membership record could not be found. Please contact an administrator.")
        return

    while True:
        print("\n--- Student Menu ---")
        print("1. View My Membership Details")
        print("2. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            member = get_member_by_id(read_members(), member_id)
            if member is None:
                print("Your membership record no longer exists. Please contact an administrator.")
                break
            display_member(member)
        elif choice == "2":
            print("Logged out.")
            break
        else:
            print("Invalid option. Please choose 1 or 2.")


# Admin: members (Create / Read / Update / Delete)
# This section of code let an admin register a student and set their password.
def admin_register_student():
    print("\n=== Admin: Register New Student ===")
    members = read_members()
    details = collect_member_details()

    username = get_unique_student_username()
    print("Set a password for the student.")
    password = get_new_password()

    member_id = generate_member_id(members)
    member = [member_id] + details + [date.today().isoformat()]

    print("\nPlease review the details:")
    display_member(member)
    print(f"Username: {username}")
    print("Password: (set by administrator)")
    if input("Confirm registration? (Y/N): ").strip().lower() != "y":
        print("Registration cancelled.")
        return

    members.append(member)
    if not save_members(members):
        print("Registration was not completed because the member file could not be saved.")
        return

    if not add_student_account(username, password, member_id):
        # Roll back the member record if account creation fails.
        members.pop()
        save_members(members)
        print("Account creation failed. Registration was rolled back.")
        return

    print(f"Student registered successfully. Member ID: {member_id}")
    print(f"Username: {username}")
    print("Please give the student their username and password securely.")


def view_all_members():
    print_member_table(read_members())

def search_by_id():
    members = read_members()
    member_id = input("Enter Member ID: ").strip()
    member = get_member_by_id(members, member_id)
    if member:
        display_member(member)
    else:
        print("No member found with that ID.")

def search_by_name():
    members = read_members()
    name = input("Enter full or partial name: ").strip().lower()
    if not name:
        print("Search term cannot be empty.")
        return
    matches = [member for member in members if name in member[1].lower()]
    print_member_table(matches)

def read_menu():
    while True:
        print("\n--- Admin Read Menu ---")
        print("1. View All Members")
        print("2. Search by Member ID")
        print("3. Search by Name")
        print("4. Return")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_members()
        elif choice == "2":
            search_by_id()
        elif choice == "3":
            search_by_name()
        elif choice == "4":
            break
        else:
            print("Invalid option. Please choose 1-4.")

# This section of code finds a member and allow the administrator to edit selected details.
def update_member():
    members = read_members()

    if not members:
        print("There are no member records to update.")
        return

    member_id = input("Enter the Member ID to update: ").strip()
    member = get_member_by_id(members, member_id)

    if member is None:
        print("Member not found.")
        return

    print("\nCurrent member information:")
    display_member(member)

    print("\nWhich information would you like to update?")
    print("1. Name")
    print("2. Age")
    print("3. Gender")
    print("4. Contact Number")
    print("5. Email")
    print("6. All editable information")
    print("7. Cancel")
    choice = input("Choose an option: ").strip()

    # Work on a copy so the original record remains unchanged until confirmation.
    updated_member = member.copy()

    if choice == "1":
        updated_member[1] = get_non_empty("Enter new name: ", "Name")
    elif choice == "2":
        updated_member[2] = get_age()
    elif choice == "3":
        updated_member[3] = get_gender()
    elif choice == "4":
        updated_member[4] = get_contact()
    elif choice == "5":
        updated_member[5] = get_email()
    elif choice == "6":
        updated_member[1] = get_non_empty("Enter new name: ", "Name")
        updated_member[2] = get_age()
        updated_member[3] = get_gender()
        updated_member[4] = get_contact()
        updated_member[5] = get_email()
    elif choice == "7":
        print("Update cancelled.")
        return
    else:
        print("Invalid option. Update cancelled.")
        return

    print("\nUpdated member information:")
    display_member(updated_member)

    if input("Save these changes? (Y/N): ").strip().lower() != "y":
        print("Update cancelled. The original record was kept.")
        return

    for index, existing_member in enumerate(members):
        if existing_member[0].lower() == member_id.lower():
            members[index] = updated_member
            break

    if save_members(members):
        print("Member information updated successfully.")
    else:
        print("Update cancelled.")

# This section of code delete a member after displaying the record and asking for confirmation.
def delete_member():
    members = read_members()

    if not members:
        print("There are no member records to delete.")
        return

    member_id = input("Enter the Member ID to delete: ").strip()
    member = get_member_by_id(members, member_id)

    if member is None:
        print("Member not found.")
        return

    print("\nThe following member will be deleted:")
    display_member(member)
    print("WARNING: This action cannot be undone.")

    if input("Confirm deletion? (Y/N): ").strip().lower() != "y":
        print("Deletion cancelled. No records were changed.")
        return

    remaining_members = [
        row for row in members if row[0].lower() != member_id.lower()
    ]

    if not save_members(remaining_members):
        print("The member record could not be deleted.")
        return

    # Remove the student login linked to this Member ID, if one exists.
    links = read_rows(LINK_FILE, 2)
    usernames_to_remove = [
        link[0] for link in links if link[1].lower() == member_id.lower()
    ]
    remaining_links = [
        link for link in links if link[1].lower() != member_id.lower()
    ]

    if not write_rows(LINK_FILE, LINK_HEADER, remaining_links):
        print("Member deleted, but the student link file could not be updated.")
        return

    accounts = read_accounts(STUDENT_FILE)
    remaining_accounts = [
        account for account in accounts
        if account[0].lower() not in
        [username.lower() for username in usernames_to_remove]
    ]

    if not write_rows(STUDENT_FILE, ACCOUNT_HEADER, remaining_accounts):
        print("Member deleted, but the student account file could not be updated.")
        return

    print("Member record deleted successfully.")
    if usernames_to_remove:
        print("The linked student login account was also deleted.")
    else:
        print("No student login account was linked to this member.")


# Admin: accounts, login and menu
# This section of code create the first administrator when none exists yet.
def setup_first_admin():
    if read_accounts(ADMIN_FILE):
        return

    print("\n=== First-Time Administrator Setup ===")
    print("No administrator account exists yet.")
    username = get_non_empty("Create admin username: ", "Username")
    password = get_new_password()
    if add_account(ADMIN_FILE, username, password):
        print("Administrator account created. Please log in.")
    else:
        print("Unable to create administrator account.")

# This section of code create a new administrator account after confirmation.
def create_admin():
    print("\n=== Admin: Create New Administrator ===")
    while True:
        username = get_non_empty("New admin username: ", "Username")
        if any(admin[0].lower() == username.lower()
               for admin in read_accounts(ADMIN_FILE)):
            print("That username is already in use.")
        else:
            break

    password = get_new_password()

    print(f"\nA new administrator account will be created for: {username}")
    if input("Confirm creation? (Y/N): ").strip().lower() != "y":
        print("Creation cancelled. No account was added.")
        return

    if add_account(ADMIN_FILE, username, password):
        print("Administrator account created successfully.")
    else:
        print("Unable to create administrator account.")

def admin_login():
    print("\n=== Admin Login ===")
    username = input("Admin username: ").strip()
    password = input("Admin password: ")
    if authenticate(ADMIN_FILE, username, password):
        print("Admin login successful.")
        admin_menu()
    else:
        print("Invalid admin username or password.")

def admin_menu():
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Create Member")
        print("2. Read Member Records")
        print("3. Update Member")
        print("4. Delete Member")
        print("5. Create Administrator")
        print("6. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            admin_register_student()
        elif choice == "2":
            read_menu()
        elif choice == "3":
            update_member()
        elif choice == "4":
            delete_member()
        elif choice == "5":
            create_admin()
        elif choice == "6":
            print("Admin logged out.")
            break
        else:
            print("Invalid option. Please choose 1-6.")