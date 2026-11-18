#!/usr/bin/python3
# Merged Login & Account Management Module (Elwin's login integrated with mainmenu)
import member


def is_admin(username):
    """Check if username exists in admins.txt (Elwin's ADMIN_FILE)."""
    member.initialise_files()
    admins = member.read_accounts(member.ADMIN_FILE)
    return any(admin[0].lower() == username.strip().lower() for admin in admins)


def is_student(username):
    """Check if username exists in student_accounts.txt (Elwin's STUDENT_FILE)."""
    member.initialise_files()
    students = member.read_accounts(member.STUDENT_FILE)
    return any(stu[0].lower() == username.strip().lower() for stu in students)


def list_admins(current_username):
    admins = member.read_accounts(member.ADMIN_FILE)
    print("\n--- Administrator Accounts ---")
    for number, admin in enumerate(admins, start=1):
        marker = " (you)" if admin[0].lower() == current_username.lower() else ""
        print(f"{number}. {admin[0]}{marker}")
    print("------------------------------")
    return admins


def remove_admin(current_username):
    print("\n=== Admin: Remove Another Administrator ===")
    admins = list_admins(current_username)

    if len(admins) <= 1:
        print("You are the only administrator, so no one can be removed.")
        return

    target = input("Enter the username to remove: ").strip()
    if not target:
        print("Username cannot be empty.")
        return

    if target.lower() == current_username.lower():
        print("You cannot remove yourself here. "
              "Use 'Delete My Own Account' from the menu instead.")
        return

    if not any(admin[0].lower() == target.lower() for admin in admins):
        print("Administrator not found.")
        return

    print(f"\nThe administrator account '{target}' will be deleted.")
    print("WARNING: This action cannot be undone.")
    if input("Confirm removal? (Y/N): ").strip().lower() != "y":
        print("Removal cancelled. No accounts were changed.")
        return

    remaining = [a for a in admins if a[0].lower() != target.lower()]
    if member.write_rows(member.ADMIN_FILE, member.ACCOUNT_HEADER, remaining):
        print("Administrator account removed successfully.")
    else:
        print("The administrator account could not be removed.")


def delete_own_account(current_username):
    print("\n=== Admin: Delete My Own Account ===")
    admins = member.read_accounts(member.ADMIN_FILE)

    if len(admins) <= 1:
        print("You are the only administrator, so your account cannot be deleted.")
        print("Create another administrator account first.")
        return False

    print(f"Your account '{current_username}' will be permanently deleted "
          "and you will be logged out.")
    print("WARNING: This action cannot be undone.")
    if input("Confirm deletion of your own account? (Y/N): ").strip().lower() != "y":
        print("Deletion cancelled. Your account was kept.")
        return False

    remaining = [a for a in admins if a[0].lower() != current_username.lower()]
    if member.write_rows(member.ADMIN_FILE, member.ACCOUNT_HEADER, remaining):
        print("Your administrator account has been deleted.")
        return True

    print("Your account could not be deleted.")
    return False


def student_login():
    from main import mainmenu
    print("\n=== Student Login ===")
    username = input("Username: ").strip()
    password = input("Password: ")
    member_id = member.find_student_member_id(username, password)

    if member_id is None:
        print("Invalid username or password.")
        return

    rec = member.get_member_by_id(member.read_members(), member_id)
    if rec is None:
        print("Your membership record could not be found. Please contact an administrator.")
        return

    print("Student login successful.")
    mainmenu(username)


def admin_login():
    from main import mainmenu
    print("\n=== Admin Login ===")
    username = input("Admin username: ").strip()
    password = input("Admin password: ")
    if member.authenticate(member.ADMIN_FILE, username, password):
        print("Admin login successful.")
        mainmenu(username)
    else:
        print("Invalid admin username or password.")


def change():
    print("\n=== Change Password ===")
    print("1. Student Account")
    print("2. Admin Account")
    role_choice = input("Select account type (1/2): ").strip()

    if role_choice == "1":
        target_file = member.STUDENT_FILE
    elif role_choice == "2":
        target_file = member.ADMIN_FILE
    else:
        print("Invalid selection.")
        return

    username = input("Enter username: ").strip()
    old_password = input("Enter current password: ")

    if not member.authenticate(target_file, username, old_password):
        print("Username or current password incorrect.")
        return

    new_password = member.get_new_password()
    salt, digest = member.hash_password(new_password)

    accounts = member.read_accounts(target_file)
    for account in accounts:
        if account[0].lower() == username.lower():
            account[1] = salt
            account[2] = digest
            break

    if member.write_rows(target_file, member.ACCOUNT_HEADER, accounts):
        print("Password changed successfully!")
    else:
        print("Unable to update password.")


def loginmenu():
    member.initialise_files()
    member.setup_first_admin()

    while True:
        print("\n===================================")
        print(" COMMUNITY LEARNING HUB LOGIN MENU")
        print("===================================")
        print("1. Student Registration")
        print("2. Student Login")
        print("3. Admin Login")
        print("4. Change Password")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            member.student_register()
        elif choice == "2":
            student_login()
        elif choice == "3":
            admin_login()
        elif choice == "4":
            change()
        elif choice == "5":
            print("Thank you for using the system.")
            raise SystemExit
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    loginmenu()
