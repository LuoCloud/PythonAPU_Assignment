# Experimental_v1.py for Create in CRUD System
# Member Management - CREATE operation
# Registers a new member in members.txt.

from datetime import datetime

# Constants
MEMBER_FILE = "members.txt"
LOG_FILE = "operations_log.txt"
MEMBER_HEADER = "MemberID|Name|Age|ContactNumber|Email|StartDate\n"
SEPARATOR = "|"

# Create the member file with a header if it does not exist.
def initialise_member_file():
    try:
        with open(MEMBER_FILE, "x", encoding="utf-8") as file:
            file.write(MEMBER_HEADER)
    except FileExistsError:
        pass
    except OSError:
        print("Error: Unable to initialise the member file.")
        return False

    return True

# Write an operation to the audit log.
def log_operation(action, record_id, details, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    details = details.replace("|", "/")

    log_entry = (
        timestamp + "|Member Management|" + action + "|"
        + record_id + "|" + details + "|" + status + "\n"
    )

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(log_entry)
    except OSError:
        print("Warning: The operation log could not be written.")

# Read existing member records.
def read_members():
    members = []

    try:
        with open(MEMBER_FILE, "r", encoding="utf-8") as file:
            header = file.readline().strip()

            if header != MEMBER_HEADER.strip():
                print("Error: The member file header is invalid.")
                return None

            for line in file:
                line = line.strip()

                if line == "":
                    continue

                member = line.split(SEPARATOR)

                # Every member must have exactly six fields.
                if len(member) != 6:
                    print("Error: A member record is malformed.")
                    return None

                if member[0] == "":
                    print("Error: A member ID is missing.")
                    return None

                members.append(member)

    except OSError:
        print("Error: Unable to read the member file.")
        return None

    return members

# Generate the next Member ID from existing records.
def generate_member_id(members):
    highest_number = 0

    for member in members:
        member_id = member[0]

        # Only accept IDs in the format M followed by digits.
        if (len(member_id) > 1 and member_id[0] == "M"
                and member_id[1:].isdigit()):
            number = int(member_id[1:])

            if number > highest_number:
                highest_number = number

    return "M" + str(highest_number + 1).zfill(4)

# Collect and validate a non-empty text field.
def get_text(prompt, field_name):
    while True:
        value = input(prompt).strip()

        if value == "":
            print("Error: " + field_name + " cannot be empty.")
        elif SEPARATOR in value or "\n" in value or "\r" in value:
            print("Error: Please do not use the | character.")
        else:
            return value

# Validate and collect the member's age.
def get_age():
    while True:
        age_text = input("Enter age (18-50): ").strip()

        try:
            age = int(age_text)

            if 18 <= age <= 50:
                return age

            print("Error: Age must be between 18 and 50.")

        except ValueError:
            print("Error: Enter a whole number for age.")

# Validate a plausible contact number.
def get_contact():
    while True:
        contact = input("Enter contact number: ").strip()

        digits = contact.replace("+", "", 1)

        if (digits.isdigit() and
                7 <= len(digits.replace("+", "")) <= 15 and
                contact.count("+") <= 1 and
                (not contact.startswith("+") or contact[1:].isdigit())):
            return contact

        print("Error: Enter a valid contact number (7-15 digits).")

# Validate a basic email format.
def get_email():
    while True:
        email = input("Enter email address: ").strip()

        if SEPARATOR in email:
            print("Error: Email cannot contain the | character.")
            continue

        if (email.count("@") == 1 and " " not in email
                and email.index("@") > 0
                and "." in email.split("@")[1]
                and not email.split("@")[1].startswith(".")
                and not email.split("@")[1].endswith(".")):
            return email

        print("Error: Enter a plausible email address.")

# Register a new member.
def create_member():
    if not initialise_member_file():
        return

    members = read_members()

    if members is None:
        return

    print("\n=== Register New Member ===")

    name = get_text("Enter full name: ", "Name")
    age = get_age()
    contact = get_contact()
    email = get_email()

    # Use today's date for the membership start date.
    start_date = datetime.now().strftime("%Y-%m-%d")

    # Generate an ID and verify that it is not already present.
    member_id = generate_member_id(members)

    for member in members:
        if member[0] == member_id:
            print("Error: Duplicate Member ID detected.")
            log_operation(
                "REGISTER", member_id,
                "Duplicate ID detected", "FAILED"
            )
            return

    # Confirm the details before saving.
    print("\nPlease confirm the member details:")
    print("Member ID: " + member_id)
    print("Name: " + name)
    print("Age: " + str(age))
    print("Contact Number: " + contact)
    print("Email: " + email)
    print("Membership Start Date: " + start_date)

    confirmation = input("\nRegister this member? (Y/N): ").strip().upper()

    if confirmation != "Y":
        print("Registration cancelled.")
        log_operation(
            "REGISTER", member_id,
            "Registration cancelled by user", "CANCELLED"
        )
        return

    # Prepare the record in the agreed field order.
    record = (
        member_id + SEPARATOR + name + SEPARATOR
        + str(age) + SEPARATOR + contact + SEPARATOR
        + email + SEPARATOR + start_date + "\n"
    )

    try:
        # Append without overwriting existing member records.
        with open(MEMBER_FILE, "a", encoding="utf-8") as file:
            file.write(record)

    except OSError:
        print("Error: The member could not be saved.")
        log_operation(
            "REGISTER", member_id,
            "Unable to write member record", "FAILED"
        )
        return

    # Record success after the member has been saved.
    log_operation(
        "REGISTER", member_id,
        "New member registered", "SUCCESS"
    )

    print("\nMember registered successfully!")
    print("Assigned Member ID: " + member_id)


# Main menu for testing the CREATE operation.
def main():
    while True:
        print("\n=== Member Management ===")
        print("1. Register a new member")
        print("2. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            create_member()
        elif choice == "2":
            print("Exiting Member Management.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


# Start the program.
if __name__ == "__main__":
    main()