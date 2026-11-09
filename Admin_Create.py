# Administrator module for registering students and their login accounts
from datetime import date
import Common as common

def create_member():
    print("\n=== Admin: Register New Student ===")
    members = common.read_members()
    details = common.collect_member_details()

    username = common.get_unique_student_username()
    print("Set a password for the student.")
    password = common.get_new_password()

    member_id = common.generate_member_id(members)
    member = [member_id] + details + [date.today().isoformat()]

    print("\nPlease review the details:")
    common.display_member(member)
    print(f"Username: {username}")
    print("Password: (set by administrator)")
    if input("Confirm registration? (Y/N): ").strip().lower() != "y":
        print("Registration cancelled.")
        return

    members.append(member)
    if not common.save_members(members):
        print("Registration was not completed because the member file could not be saved.")
        return

    if not common.add_student_account(username, password, member_id):
        # Roll back the member record if account creation fails.
        members.pop()
        common.save_members(members)
        print("Account creation failed. Registration was rolled back.")
        return

    print(f"Student registered successfully. Member ID: {member_id}")
    print(f"Username: {username}")
    print("Please give the student their username and password securely.")