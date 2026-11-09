# Administrator account management module. Only an authenticated administrator should call these functions.
import Common as common

# This section of code display all administrator usernames and mark the current one.
def list_admins(current_username):
    admins = common.read_accounts(common.ADMIN_FILE)
    print("\n--- Administrator Accounts ---")
    for number, admin in enumerate(admins, start=1):
        marker = " (you)" if admin[0].lower() == current_username.lower() else ""
        print(f"{number}. {admin[0]}{marker}")
    print("------------------------------")
    return admins

# This section of code create a new administrator account after confirmation.
def create_admin():
    print("\n=== Admin: Create New Administrator ===")
    while True:
        username = common.get_non_empty("New admin username: ", "Username")
        if any(admin[0].lower() == username.lower()
               for admin in common.read_accounts(common.ADMIN_FILE)):
            print("That username is already in use.")
        else:
            break

    password = common.get_new_password()

    print(f"\nA new administrator account will be created for: {username}")
    if input("Confirm creation? (Y/N): ").strip().lower() != "y":
        print("Creation cancelled. No account was added.")
        return

    if common.add_account(common.ADMIN_FILE, username, password):
        print("Administrator account created successfully.")
    else:
        print("Unable to create administrator account.")

# This section of code remove another administrator after confirmation.
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

    if common.remove_account(common.ADMIN_FILE, target):
        print("Administrator account removed successfully.")
    else:
        print("The administrator account could not be removed.")

# This section of code let an administrator delete their own account. Returns True if the account was deleted, so the caller can log out.
def delete_own_account(current_username):
    print("\n=== Admin: Delete My Own Account ===")
    admins = common.read_accounts(common.ADMIN_FILE)

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

    if common.remove_account(common.ADMIN_FILE, current_username):
        print("Your administrator account has been deleted.")
        return True

    print("Your account could not be deleted.")
    return False