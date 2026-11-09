# Student login and own-record viewing module
import Common as common

def student_login():
    print("\n=== Student Login ===")
    username = input("Username: ").strip()
    password = input("Password: ")
    member_id = common.find_student_member_id(username, password)

    if member_id is None:
        print("Invalid username or password.")
        return

    members = common.read_members()
    member = common.get_member_by_id(members, member_id)
    if member is None:
        print("Your membership record could not be found. Please contact an administrator.")
        return

    while True:
        print("\n--- Student Menu ---")
        print("1. View My Membership Details")
        print("2. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            member = common.get_member_by_id(common.read_members(), member_id)
            if member is None:
                print("Your membership record no longer exists. Please contact an administrator.")
                break
            common.display_member(member)
        elif choice == "2":
            print("Logged out.")
            break
        else:
            print("Invalid option. Please choose 1 or 2.")