# Note for Li Ting: You need to
# 1. Change return to LMS menu in main, admin and user coursemenu to go to your menu
# 2. Do ur magic on the password thing in main coursemenu
# If you need help or have any questions let me know ill be glad to help in any way I can

# Hiearchical Imports
from cmdatabase import load_coursedata
from cmcontroller import addcourse
from cmcontroller import updatecourse
from cmcontroller import deletecourse
from cmcontroller import viewcourse


# Main menu asking if you are admin or user
def main_coursemenu():
    print("=== Role Selection Menu ===\n"
          "1. User\n"
          "2. Admin\n"
          "3. Press Q to return to LMS Menu.\n")

    while True:
        role = input("\nSelection: ")

        # Validation Block
        if role not in ("1", "2", "3"):
            print("Input is invalid. Select 1, 2 or 3")

        elif role == "1":
            print("\nWhat is your password?")
            password = input("Password: ")
            # If password is wrong, loop until right
            # If password is right, let them pass
            print("\nTaking you to the user menu...")
            user_coursemenu()

        elif role == "2":
            print("\nWhat is your admin key?")
            adminkey = input("Admin Key: ")
            # If adminkey is wrong, loop until right
            # If adminkey is right, let them pass
            print("\nTaking you to the admin menu...")
            admin_coursemenu()

        elif role == "3":
            print("\nReturning to LMS Menu...")
            #Return back to LTs Main Menu
            break
# Displays the course management system menu
# Checks and validates the role before letting them access the CMS

# Menu interface for Admins
def admin_coursemenu():

    #Load current courses into memory
    coursedata = load_coursedata()

    while True:
        print(
            "\n==== Course Management System (Admin) ====\n"
            "1. Press 1 to add a course\n"
            "2. Press 2 to edit a course\n"
            "3. Press 3 to remove a course\n"
            "4. Press 4 to view existing courses\n"
            "5. Press 5 to return to LMS Menu\n"
            "6. Press 6 to return to role selection\n"
        )

        #Validation block
        while True:
            viewcourse_selection = input("\nChoose an option: ")
            if viewcourse_selection.isalpha():
                print("Option cannot contain letters.")
            elif viewcourse_selection == "":
                print("Option cannot be empty.")
            elif viewcourse_selection in ("1", "2", "3", "4", "5", "6"):
                break
            else:
                print("Invalid Option. Try Again.")

        #Selects a function or returns to Main Menu
        if viewcourse_selection == "1":
            addcourse(coursedata)
        elif viewcourse_selection == "2":
            updatecourse(coursedata)
        elif viewcourse_selection == "3":
            deletecourse(coursedata)
        elif viewcourse_selection == "4":
            viewcourse(coursedata)
        elif viewcourse_selection == "5":
            print("\nReturning to LMS Menu...")
            #Return back to LTs Main Menu
            break
        elif viewcourse_selection == "6":
            main_coursemenu()
# Displays the functions admins can use

# Menu interface for Admins
def user_coursemenu():

    #Load current courses into memory
    coursedata = load_coursedata()

    while True:
        print(
            "\n==== Course Management System (Admin) ====\n"
            "1. Select 1 to view existing courses\n"
            "2. Select 2 to return to LMS Menu\n"
            "3. Select 3 to return to role selection\n"
        )

        #Validation block
        while True:
            viewcourse_selection = input("\nChoose an option: ")
            if viewcourse_selection.isalpha():
                print("Option cannot contain letters.")
            elif viewcourse_selection == "":
                print("Option cannot be empty.")
            elif viewcourse_selection in ("1", "2", "3"):
                break
            else:
                print("Invalid Option. Try Again.")

        #Selects a function or returns to Main Menu
        if viewcourse_selection == "1":
            viewcourse(coursedata)
        elif viewcourse_selection == "2":
            print("\nReturning to LMS Menu...")
            #Return back to LTs Main Menu
            break
        elif viewcourse_selection == "3":
            main_coursemenu()
# Displays the functions users can use


main_coursemenu()