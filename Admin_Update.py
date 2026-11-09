# Administrator update module. Only an authenticated administrator should call update_member().
import Common as common

# This section of code finds a member and allow the administrator to edit selected details.
def update_member():
    members = common.read_members()

    if not members:
        print("There are no member records to update.")
        return

    member_id = input("Enter the Member ID to update: ").strip()
    member = common.get_member_by_id(members, member_id)

    if member is None:
        print("Member not found.")
        return

    print("\nCurrent member information:")
    common.display_member(member)

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
        updated_member[1] = common.get_non_empty("Enter new name: ", "Name")
    elif choice == "2":
        updated_member[2] = common.get_age()
    elif choice == "3":
        updated_member[3] = common.get_gender()
    elif choice == "4":
        updated_member[4] = common.get_contact()
    elif choice == "5":
        updated_member[5] = common.get_email()
    elif choice == "6":
        updated_member[1] = common.get_non_empty("Enter new name: ", "Name")
        updated_member[2] = common.get_age()
        updated_member[3] = common.get_gender()
        updated_member[4] = common.get_contact()
        updated_member[5] = common.get_email()
    elif choice == "7":
        print("Update cancelled.")
        return
    else:
        print("Invalid option. Update cancelled.")
        return

    print("\nUpdated member information:")
    common.display_member(updated_member)

    if input("Save these changes? (Y/N): ").strip().lower() != "y":
        print("Update cancelled. The original record was kept.")
        return

    for index, existing_member in enumerate(members):
        if existing_member[0].lower() == member_id.lower():
            members[index] = updated_member
            break

    if common.save_members(members):
        print("Member information updated successfully.")
    else:
        print("Update cancelled.")