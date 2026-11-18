# Note: coursedata is the local storage (volatile), cmstorage.txt is the external storage (non-volatile).
# Weak warnings in the top are just broad exception clauses from try, except.
# Dictionary keys for coursedata: "courname", "courinstructor", "courduration", "courfee", "courcapacity"

# Hiearchical Imports
from cmdatabase import save_coursedata
from cmdatabase import extra_maximumcourse

# Function for adding courses
def addcourse(coursedata):

    #Asking for course quantity to add, then validating
    while True:
        try:
            courseamount = int(input("\nHow many courses would you like to add?: "))
            # Checks if the courses will hit the maximum (20 courses)
            if extra_maximumcourse(courseamount) == "Limit reached":
                return
            if courseamount < 0:
                print("Course amount cannot be negative. Try again.")
            elif courseamount == 0:
                print("Course amount cannot be 0. Try again.")
            # Avoiding bulk course adding.
            elif courseamount > 3:
                print("Please add a few courses at a time. Try again.")
            else:
                print("Successfully inputed!")
                break
        except:
            print("Input must be a number between 1-3. Try again.")


    #As long as the course amount is not 0, loop through inputs
    while courseamount != 0:
        while True:
            courseid = str(input("\nCourse ID (e.g. (092026-MAL)): "))
            if courseid.strip() == "":
                print("Provide a valid course ID. Try again.")
            elif courseid in coursedata:
                print("Course already exists. Use another ID.")
            else:
                print("Successfully inputed!")
                break

        while True:
            coursename = str(input("\nCourse Name (e.g. Programming With Python): "))
            if coursename.strip() == "":
                print("Provide a valid course name. Try again.")
            else:
                print("Successfully inputed!")
                break

        while True:
            courseinstructor = str(input("\nInstructor (e.g. Dr Masrina): "))
            if courseinstructor.strip() == "":
                print("Provide a valid course instructor.")
            elif len(courseinstructor) > 0:
                print("Successfully inputed!")
                break
            else:
                print("Invalid input. Try again.")

        while True:
            coursedur = str(input("\nCourse Duration (e.g. 4 Months): "))
            if coursedur.strip() == "":
                print("Provide a valid course duration.")
            elif coursedur.isalpha():
                print("Provide a valid course duration.")
            elif len(coursedur) < 15:
                print("Successfully inputed!")
                break
            else:
                print("Invalid input. Try again.")

        while True:
            try:
                coursefee = float(input("\nCourse Fee (e.g. 3000): "))
                if coursefee < 0:
                    print("Course fee cannot be negative.")
                else:
                    coursefee = f"RM{coursefee:.2f}"
                    print("Successfully inputed!")
                    break
            except:
                print("Input must be a number. Try again.")

        while True:
            try:
                coursecap = int(input("\nMaximum Student Capacity (e.g. 30): "))
                if coursecap < 0:
                    print("Course capacity cannot be negative.")
                else:
                    print("Successfully inputed!")
                    break
            except:
                print("Input must be a number. Try again.")

        # Storing inputs into coursedata
        courseinputs = {
            courseid : {
                "courname" : coursename,
                "courinstructor" : courseinstructor,
                "courduration" : coursedur,
                "courfee" : coursefee,
                "courcapacity" : coursecap,
                        }}
        coursedata.update(courseinputs)

        #Store course
        if courseamount > 1:
            save_coursedata(coursedata)
            courseamount -= 1
            print("\nProvide details for the next course.\n")
        else:
            save_coursedata(coursedata)
# Adds 1 or more courses into cmstorage.txt

# Course edit menu for updatecourse()
def courseeditmenu():
    print("\nWhich section would you like to edit?\n"
          "Input 1 to edit Course Name\n"
          "Input 2 to edit Course Instructor\n"
          "Input 3 to edit Course Duration\n"
          "Input 4 to edit Course Fee\n"
          "Input 5 to edit Course Capacity\n"
          "Input Q to return to Main Menu")

    while True:
        courseedit_selection = input("\nSelection: ")

        # Validation to ensure correct value is given to update function
        if courseedit_selection.upper() == "Q":
            return courseedit_selection
        elif courseedit_selection == "1":
            return courseedit_selection
        elif courseedit_selection == "2":
            return courseedit_selection
        elif courseedit_selection == "3":
            return courseedit_selection
        elif courseedit_selection == "4":
            return courseedit_selection
        elif courseedit_selection == "5":
            return courseedit_selection
        else:
            print("Invalid input. Try again.")
# Displays the course edit function menu

# Function for updating courses
def updatecourse(coursedata):

    #Checking if memory is empty
    if coursedata == {}:
        print("There are currently no courses in storage.\n"
              "Add a course, or contact an Admin for further support")
        return

    while True:
        #Asking for course id to make changes
        courseid_selection = input("\nPlease insert your Course ID to edit: ")
        if courseid_selection.isdigit():
            print("Invalid Course ID")
        elif courseid_selection not in coursedata:
            print("Course is not listed in database. Try again.")
        elif courseid_selection in coursedata:
            break

    #Block for course name editing
    while True:
        courseedit_selection = courseeditmenu()
        while courseedit_selection == "1":
            newcoursename = input("\nNew Course Name: ")

            #Validation block
            if newcoursename.strip() == "":
                print("Input is empty, please try again.")
            elif newcoursename.isdigit():
                print("Input cannot be a number, please try again.")
            else:
                coursedata[courseid_selection]["courname"] = newcoursename
                print("\nCourse Name Successfully Updated.")
                break

        #Block for course instructor editing
        while courseedit_selection == "2":
            newcourseinstructor = input("\nNew Course Instructor: ")

            #Validation block
            if newcourseinstructor.strip() == "":
                print("Input is empty, please try again.")
            elif newcourseinstructor.isdigit():
                print("Input cannot be a number, please try again.")
            else:
                coursedata[courseid_selection]["courinstructor"] = newcourseinstructor
                print("\nCourse Instructor Successfully Updated.")
                break

        #Block for course duration editing
        while courseedit_selection == "3":
            newcourseduration = input("\nNew Course Duration: ")

            #Validation block
            if newcourseduration.strip() == "":
                print("Input is empty, please try again.")
            elif newcourseduration.isdigit():
                print("Input cannot be a number, please try again.")
            else:
                coursedata[courseid_selection]["courduration"] = newcourseduration
                print("\nCourse Duration Successfully Updated.")
                break

        #Block for course fee editing
        while courseedit_selection == "4":
            try:
                newcoursefee = float(input("\nNew Course Fee: "))

                #Validation block
                if newcoursefee < 0:
                    print("Input cannot be negative. Try again.")
                else:
                    newcoursefee = f"RM{newcoursefee:.2f}"
                    coursedata[courseid_selection]["courfee"] = newcoursefee
                    print("\nCourse Fee Successfully Updated.")
                    break
            except:
                print("Please input a number. Try again.")

        #Block for course capacity editing
        while courseedit_selection == "5":
            try:
                newcoursecapacity = int(input("\nNew Course Capacity: "))

                #Validation block
                if "" in newcoursecapacity:
                    print("Input is empty, please try again.")
                elif newcoursecapacity < 0:
                    print("Course capacity cannot be a negative value. Try again.")
                else:
                    coursedata[courseid_selection]["courcapacity"] = newcoursecapacity
                    print("\nCourse Capacity Successfully Updated.")
                    break
            except:
                print("Please input a number. Try again.")

        #Return to menu function
        if courseedit_selection.upper() == "Q":
            print("\nReturning to Main Menu...\n")
            #Save to external file
            save_coursedata(coursedata)
            break
# Allows for pinpointing within the dictionary to make changes

# Course delete menu for deletecourse()
def coursedeletemenu():
    print("\n---Course Delete Menu---\n"
          "Input 1 to view courses\n"
          "Input 2 to delete course\n")

    while True:
        coursedelete_menuoption = input("Selection: ")

        # Validation to ensure correct value is given to update function
        if coursedelete_menuoption.upper() == "Q":
            return coursedelete_menuoption
        elif coursedelete_menuoption == "1":
            return coursedelete_menuoption
        elif coursedelete_menuoption == "2":
            return coursedelete_menuoption
        else:
            print("Invalid input. Try again.")
# Displays the delete course function menu

# Function for deleting courses
def deletecourse(coursedata):

    #Checking if memory is empty
    if coursedata == {}:
        print("There are currently no courses in storage.\n"
              "Add a course, or contact an Admin for further support")
        return

    # Summoning the menu and collecting its input
    coursedelete_menuoption = coursedeletemenu()

    # Validation for menu input
    #Making sure that its 1 or 2 as the input
    while coursedelete_menuoption != "1" and coursedelete_menuoption != "2":
        print("Input is invalid. Try again")
        coursedelete_menuoption = coursedeletemenu()

    # Scenario 1, view
    if coursedelete_menuoption == "1":
        while True:
            try:
                coursedelete_viewcourse = input("Would you like to view courses? (Y/N): ")
                if coursedelete_viewcourse.upper() == "Y":
                    print("Retrieving courses...")
                    viewcourse(coursedata)
                    break
                elif coursedelete_viewcourse.upper() == "N":
                    print("Proceeding to deletion...")
                    break
            except:
                print("Invalid input. Try again.")

    # Scenario 2, delete
    elif coursedelete_menuoption == "2":
        while True:
            deletecourse_input = input("Which course would you like to delete?: ")
            if deletecourse_input not in coursedata:
                print("Course is not in database. Try Again.")
            elif deletecourse_input == "":
                print("Input cannot be empty.")
            elif deletecourse_input.isdigit():
                print("Invalid Input.")
            else:
                break

        # Delete confirmation
        while True:
            if deletecourse_input in coursedata and deletecourse_input != "":
                deletecourse_confirmation = input("Are you sure you would like to delete "f"{deletecourse_input}? (Y/N): ")
                if deletecourse_confirmation.upper() == "Y":
                    coursedata.__delitem__(deletecourse_input)
                    print("\nCourse has been removed. Saving and returning to Main Menu...\n")
                    break
                elif deletecourse_confirmation.upper() == "N":
                    print("\nCourse deletion cancelled. Returning to Main Menu...\n")
                    return
                else:
                    print("Input is invalid. Input Y or N.")

        # Save to External File
        # Saving is placed here to ensure the data has been properly validated.
        save_coursedata(coursedata)
        return
# Allows admin to delete a course, confirmation is asked to the admin.

# Function for viewing courses
def viewcourse(coursedata):

    counter = 1
    if coursedata == {}:
        print("\nNo courses available to view at this time.")
    for key, value in coursedata.items():
        formattedcoursedata = (f"Course: {key}\n"
                f"Course Name: {value["courname"]}\n"
                f"Course Instructor: {value["courinstructor"]}\n"
                f"Course Duration: {value["courduration"]}\n"
                f"Course Fee: {value["courfee"]}\n"
                f"Course Capacity: {value["courcapacity"]}\n")
        print(f"{counter}.")
        print(formattedcoursedata)
        counter += 1
# Formats courses from cmstorage.txt into clean blocks of string.
