# Main controller for the Community Learning Hub system
import Common as common
import Student_Create as student_create
import Student_Read as student_read
import Admin_Create as admin_create
import Admin_Read as admin_read
import Admin_Update as admin_update
import Admin_Delete as admin_delete
import Admin_Accounts as admin_accounts

def setup_first_admin():
    admins = common.read_accounts(common.ADMIN_FILE)
    if admins:
        return

    print("\n=== First-Time Administrator Setup ===")
    print("No administrator account exists yet.")
    username = common.get_non_empty("Create admin username: ", "Username")
    password = common.get_new_password()
    if common.add_account(common.ADMIN_FILE, username, password):
        print("Administrator account created. Please log in.")
    else:
        print("Unable to create administrator account.")

def admin_login():
    print("\n=== Admin Login ===")
    username = input("Admin username: ").strip()
    password = input("Admin password: ")
    if common.authenticate(common.ADMIN_FILE, username, password):
        print("Admin login successful.")
        admin_menu(username)
    else:
        print("Invalid admin username or password.")

def admin_menu(current_username):
    while True:
        print("\n===== ADMIN MENU =====")
        print("1. Create Member")
        print("2. Read Member Records")
        print("3. Update Member")
        print("4. Delete Member")
        print("5. Create Administrator")
        print("6. Remove Another Administrator")
        print("7. Delete My Own Account")
        print("8. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            admin_create.create_member()
        elif choice == "2":
            admin_read.read_menu()
        elif choice == "3":
            admin_update.update_member()
        elif choice == "4":
            admin_delete.delete_member()
        elif choice == "5":
            admin_accounts.create_admin()
        elif choice == "6":
            admin_accounts.remove_admin(current_username)
        elif choice == "7":
            if admin_accounts.delete_own_account(current_username):
                print("Admin logged out.")
                break  # Account is gone, so end the session.
        elif choice == "8":
            print("Admin logged out.")
            break
        else:
            print("Invalid option. Please choose 1-8.")

def main():
    common.initialise_files()
    setup_first_admin()

    while True:
        print("\n===================================")
        print(" COMMUNITY LEARNING HUB SYSTEM")
        print("===================================")
        print("1. Student Registration")
        print("2. Student Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            student_create.create_member()
        elif choice == "2":
            student_read.student_login()
        elif choice == "3":
            admin_login()
        elif choice == "4":
            print("Thank you for using the system.")
            break
        else:
            print("Invalid option. Please choose 1-4.")


if __name__ == "__main__":
    main()