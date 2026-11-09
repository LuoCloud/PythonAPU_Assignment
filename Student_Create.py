# Student self-registration module
from datetime import date
import Common as common

def create_member():
    print("\n=== Student Self-Registration ===")
    members = common.read_members()
    details = common.collect_member_details()

    while True:
        username = common.get_unique_student_username()
        if any(row[0].lower() == username.lower()
               for row in common.read_accounts(common.STUDENT_FILE)):
            print("That username is already taken.")
        else:
            break

    password = common.get_new_password()
    member_id = common.generate_member_id(members)
    member = [member_id] + details + [date.today().isoformat()]

    print("\nPlease review your details:")
    common.display_member(member)
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

    print(f"Registration successful. Your Member ID is {member_id}.")
    print("Keep your username and password safe.")