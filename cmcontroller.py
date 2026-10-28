#Adding courses (Ask for module, course, etc.)
#Suggested fields: Course ID, Course Name, Instructor, Duration, Fee, Maximum Capacity.

#Updating existing courses (be able to update the
#database file

#Delete feature that removes the data from the
#database file

#Master dictionary for courses
coursedata = {"testing":{}}

#Function for adding courses
def addcourse():
    while True:
        courseamount = int(input("How many courses would you like to add?: "))
        if courseamount < 0:
            print("Course amount cannot be negative.")
        elif courseamount > 3:
            print("Please add a few courses at a time.")
        else:
            break


    #Important to note that courseid serves as the unique key in the dictionary
    #While others will be the values to the key (courseid)
    while courseamount != 0:
        courseid = str(input("Course ID (e.g. (092026-MAL)): "))
        if courseid == "":
            print("Provide a valid course ID.")
            courseid = str(input("Course ID (e.g. (092026-MAL)): "))
        elif courseid in coursedata:
            print("Course already exists")
            courseid = str(input("Course ID (e.g. (092026-MAL)): "))
        else:
            pass
            #Add course id as key to storage

        coursename = str(input("Course Name (e.g. Programming With Python): "))
        if coursename == "":
            print("Provide a valid course name.")
            str(input("Course Name (e.g. Programming With Python): "))
        else:
            pass
            #Place coursename as value in storage

        courseinstructor = str(input("Instructor (e.g. Dr Masrina): "))
        if courseinstructor == "":
            print("Provide a valid course instructor.")
        elif courseinstructor == type(int):
            print("Provide course instructor name.")
            courseinstructor = str(input("Instructor (e.g. Dr Masrina): "))
        else:
            pass
            #Add course instructor as value to storage

        coursedur = str(input("Course Duration (e.g. 4 Months): "))
        if coursedur == "":
            print("Provide a valid course duration.")
        else:
            pass
            #Add course duration as value to storage

        coursefee = float(input("Course Fee (e.g. 3000): "))
        if coursefee == "":
            print("Provide a valid course fee.")
        elif coursefee < 0:
            print("Course fee cannot be negative.")
        else:
            pass
            #Add coursefee as value into storage with RM sign

        coursecap = int(input("Maximum Student Capacity (e.g. 30): "))
        if coursecap == "":
            print("Provide a valid course capacity.")
        elif coursecap < 0:
            print("Course capacity cannoy be negative.")
        else:
            pass
            #Add course capacity as value into storage

        courseinputs = {
            courseid : {
                "Course Name: " : coursename ,
                "Course Instructor: " : courseinstructor ,
                "Course Duration: " : coursedur ,
                "Course Fee: " : coursefee ,
                "Course Capacity" : coursecap
            }
        }

        coursedata.update(courseinputs)
        if courseamount > 1:
            courseamount -= 1
            print("\nProvide details for the next course.\n")
        else:
            courseamount -= 1
            print("\nCourses Successfully Added.\n"
                  "Returning to Main Menu...\n")
            return

#Function for updating courses (Needs to be able to pinpoint a field and edit it)
def updatecourse():
    while True:
        courseid_selection = input("Please insert your Course ID to edit: ")
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
            newcoursename = input("New Course Name: ")

            #Validation block
            if newcoursename == "":
                print("Input is empty, please try again.")
            elif newcoursename.isdigit():
                print("Input cannot be a number, please try again.")
            else:
                coursedata[courseid_selection]["Course Name: "] = newcoursename
                print("\nCourse Name Successfully Updated.\n")
                courseeditmenu()
                break

        #Block for course instructor editing
        while courseedit_selection == "2":
            newcourseinstructor = input("New Course Instructor: ")

            #Validation block
            if newcourseinstructor == "":
                print("Input is empty, please try again.")
            elif newcourseinstructor.isdigit():
                print("Input cannot be a number, please try again.")
            else:
                coursedata[courseid_selection]["Course Instructor: "] = newcourseinstructor
                print("\nCourse Instructor Successfully Updated.\n")
                courseeditmenu()
                break

        #Block for course duration editing
        while courseedit_selection == "3":
            newcourseduration = input("New Course Duration: ")

            #Validation
            if newcourseduration == "":
                print("Input is empty, please try again.")
            elif newcourseduration.isdigit():
                print("Input cannot be a number, please try again.")
            else:
                coursedata[courseid_selection]["Course Duration: "] = newcourseduration
                print("\nCourse Duration Successfully Updated.\n")
                courseeditmenu()
                break

        #Block for course fee editing
        while courseedit_selection == "4":
            newcoursefee = input("New Course Fee: ")

            #Validation
            if newcoursefee == "":
                print("Input is empty, please try again.")
            elif newcoursefee.isalpha():
                print("Input cannot be a letter, please try again.")
            else:
                coursedata[courseid_selection]["Course Fee: "] = newcoursefee
                print("\nCourse Fee Successfully Updated.\n")
                courseeditmenu()
                break

        #Block for course capacity editing
        while courseedit_selection == "5":
            newcoursecapacity = input("New Course Capacity: ")
            #Validation
            if newcoursecapacity == "":
                print("Input is empty, please try again.")
            elif newcoursecapacity.isalpha():
                print("Input cannot be a letter, please try again.")
            else:
                coursedata[courseid_selection]["Course Capacity"] = newcoursecapacity
                print("\nCourse Capacity Successfully Updated.\n")
                courseeditmenu()
                break

        if courseedit_selection.upper() == "Q":
            print("\nReturning to Main Menu...\n")
            return

#Course edit menu for updatecourse() function ^^^
def courseeditmenu():
    print("Which section would you like to edit?\n"
          "Input 1 to edit Course Name\n"
          "Input 2 to edit Course Instructor\n"
          "Input 3 to edit Course Duration\n"
          "Input 4 to edit Course Fee\n"
          "Input 5 to edit Course Capacity\n"
          "Input Q to return to Main Menu")
    courseedit_selection = input("Selection: ")
    return courseedit_selection

#Function for deleting courses
def deletecourse():
    coursedelete_menuoption = coursedeletemenu()

    #Making sure that its 1 or 2 as the input
    while coursedelete_menuoption != "1" and coursedelete_menuoption != "2":
        print("Input is invalid. Try again")
        coursedelete_viewcourse = input("Would you like to view courses? (Y/N): ")
        if coursedelete_viewcourse == "1" or coursedelete_viewcourse == "2":
            break

    #Scenario for 1 or 2 input options
    if coursedelete_menuoption == "1":
        while True:
            coursedelete_viewcourse = input("Would you like to view courses? (Y/N): ")
            if coursedelete_viewcourse.upper() == "Y":
                print("Retrieving courses...")
                viewcourse()
                break
            elif coursedelete_viewcourse.upper() == "N":
                print("Returning...")
                coursedeletemenu() #Ended off here where it only checks once
                break
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
        if deletecourse_input in coursedata and deletecourse_input != "":
            deletecourse_confirmation = input("Are you sure you would like to delete this course? (Y/N): ")
            if deletecourse_confirmation.upper() == "Y":
                coursedata.__delitem__(deletecourse_input)
                print("\nCourse has been removed. Returning to Main Menu...\n")
                return
            elif deletecourse_confirmation.upper() == "N":
                print("\nCourse deletion cancelled. Returning to Main Menu...\n")
                return

#Course delete menu for deletecourse() function ^^^
def coursedeletemenu():
    print("\n---Course Delete Menu---\n"
          "Input 1 to view courses\n"
          "Input 2 to delete course\n")
    coursedelete_menuoption = input("Selection: ")
    return coursedelete_menuoption

#Function for viewing courses
def viewcourse():
    print(coursedata)

#Menu interface
def coursemenu():
    while True:
        print(
            "---- Awesome Interface for courses!! ----\n"
            "Press 1 to add a course\n"
            "Press 2 to edit a course\n"
            "Press 3 to remove a course\n"
            "Press 4 to return to LMS Menu\n"
        )

        viewcourse_selection = input("Choose an option: ")
        if viewcourse_selection == "1":
            addcourse()
        elif viewcourse_selection == "2":
            updatecourse()
        elif viewcourse_selection == "3":
            deletecourse()
            #Return to LTs LMS Menu
        elif viewcourse_selection.isalpha():
            print("Option cannot contain letters.")
            viewcourse_selection = input("Choose an option: ")
        elif viewcourse_selection == "":
            print("Option cannot be empty.")
            viewcourse_selection = input("Choose an option: ")
        else:
            print("Invalid option")
            viewcourse_selection = input("Choose an option: ")
        if viewcourse_selection == "4":
            print("Returning to LMS Menu...")
            break

coursemenu()

