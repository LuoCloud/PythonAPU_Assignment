# Administrator read/search module
import Common as common

def view_all_members():
    members = common.read_members()
    common.print_member_table(members)

def search_by_id():
    members = common.read_members()
    member_id = input("Enter Member ID: ").strip()
    member = common.get_member_by_id(members, member_id)
    if member:
        common.display_member(member)
    else:
        print("No member found with that ID.")

def search_by_name():
    members = common.read_members()
    name = input("Enter full or partial name: ").strip().lower()
    if not name:
        print("Search term cannot be empty.")
        return
    matches = [member for member in members if name in member[1].lower()]
    common.print_member_table(matches)

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