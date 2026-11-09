# Administrator delete module. Only an authenticated administrator should call delete_member().
import Common as common

# This section of code delete a member after displaying the record and asking for confirmation.
def delete_member():
    members = common.read_members()

    if not members:
        print("There are no member records to delete.")
        return

    member_id = input("Enter the Member ID to delete: ").strip()
    member = common.get_member_by_id(members, member_id)

    if member is None:
        print("Member not found.")
        return

    print("\nThe following member will be deleted:")
    common.display_member(member)
    print("WARNING: This action cannot be undone.")

    if input("Confirm deletion? (Y/N): ").strip().lower() != "y":
        print("Deletion cancelled. No records were changed.")
        return

    remaining_members = [
        row for row in members if row[0].lower() != member_id.lower()
    ]

    if not common.save_members(remaining_members):
        print("The member record could not be deleted.")
        return

    # Remove the student login linked to this Member ID, if one exists.
    links = common.read_rows(common.LINK_FILE, 2)
    usernames_to_remove = [
        link[0] for link in links if link[1].lower() == member_id.lower()
    ]
    remaining_links = [
        link for link in links if link[1].lower() != member_id.lower()
    ]

    if not common.write_rows(
            common.LINK_FILE, common.LINK_HEADER, remaining_links):
        print("Member deleted, but the student link file could not be updated.")
        return

    accounts = common.read_accounts(common.STUDENT_FILE)
    remaining_accounts = [
        account for account in accounts
        if account[0].lower() not in
        [username.lower() for username in usernames_to_remove]
    ]

    if not common.write_rows(
            common.STUDENT_FILE, common.ACCOUNT_HEADER, remaining_accounts):
        print("Member deleted, but the student account file could not be updated.")
        return

    print("Member record deleted successfully.")
    if usernames_to_remove:
        print("The linked student login account was also deleted.")
    else:
        print("No student login account was linked to this member.")