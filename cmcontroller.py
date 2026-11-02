#Adding courses (Ask for module, course, etc.)
#Suggested fields: Course ID, Course Name, Instructor, Duration, Fee, Maximum Capacity.

#Updating existing courses (be able to update the
#database file

#Delete feature that removes the data from the
#database file

#its jason say hi
import json
from textwrap import indent

#Master dictionary for courses
coursedata = {"testing":{}}

#Function for adding courses
def addcourse():
    #Asking for course quantity to add
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
        while True:
            courseid = str(input("Course ID (e.g. (092026-MAL)): "))
            if courseid == "":
                print("Provide a valid course ID.")
            elif courseid in coursedata:
                print("Course already exists")
            else:
                break

        while True:
            coursename = str(input("Course Name (e.g. Programming With Python): "))
            if coursename == "":
                print("Provide a valid course name.")
                str(input("Course Name (e.g. Programming With Python): "))
            else:
                #Place coursename as value in storage then
                break

        while True:
            courseinstructor = str(input("Instructor (e.g. Dr Masrina): "))
            if courseinstructor == "":
                print("Provide a valid course instructor.")
            else:
                #Add course instructor as value to storage then
                break
        while True:
            coursedur = str(input("Course Duration (e.g. 4 Months): "))
            if coursedur == "":
                print("Provide a valid course duration.")
            else:
                #Add course duration as value to storage then
                break

        while True:
            coursefee = float(input("Course Fee (e.g. 3000): "))
            if coursefee == "":
                print("Provide a valid course fee.")
            elif coursefee < 0:
                print("Course fee cannot be negative.")
            else:
                #Add coursefee as value into storage with RM sign then
                break

        while True:
            coursecap = int(input("Maximum Student Capacity (e.g. 30): "))
            if coursecap == "":
                print("Provide a valid course capacity.")
            elif coursecap < 0:
                print("Course capacity cannoy be negative.")
            else:
                #Add course capacity as value into storage then
                break

        #Adding information into storage
        courseinputs = {
            courseid : {
                "Course Name: " : coursename ,
                "Course Instructor: " : courseinstructor ,
                "Course Duration: " : coursedur ,
                "Course Fee: " : coursefee ,
                "Course Capacity" : coursecap
            }
        }

        #Counter function to track if all courses have been inputed
        coursedata.update(courseinputs)
        if courseamount > 1:
            courseamount -= 1
            print("\nProvide details for the next course.\n")
            with open("cmstorage.json", "w") as file:
                json.dump(courseinputs, file, indent=4)
        else:
            courseamount -= 1
            print("\nCourses Successfully Added.\n"
                  "Returning to Main Menu...\n")
            with open("cmstorage.json", "w") as file:
                json.dump(courseinputs, file, indent=4)
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
    #Returns the input for updatecourse function
    return courseedit_selection

#Function for updating courses (Needs to be able to pinpoint a field and edit it)
def updatecourse():
    while True:
        #Asking for course id to make changes
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
                break

        #Block for course duration editing
        while courseedit_selection == "3":
            newcourseduration = input("New Course Duration: ")

            #Validation block
            if newcourseduration == "":
                print("Input is empty, please try again.")
            elif newcourseduration.isdigit():
                print("Input cannot be a number, please try again.")
            else:
                coursedata[courseid_selection]["Course Duration: "] = newcourseduration
                print("\nCourse Duration Successfully Updated.\n")
                break

        #Block for course fee editing
        while courseedit_selection == "4":
            newcoursefee = input("New Course Fee: ")

            #Validation block
            if newcoursefee == "":
                print("Input is empty, please try again.")
            elif newcoursefee.isalpha():
                print("Input cannot be a letter, please try again.")
            else:
                coursedata[courseid_selection]["Course Fee: "] = newcoursefee
                print("\nCourse Fee Successfully Updated.\n")
                break

        #Block for course capacity editing
        while courseedit_selection == "5":
            newcoursecapacity = input("New Course Capacity: ")

            #Validation block
            if newcoursecapacity == "":
                print("Input is empty, please try again.")
            elif newcoursecapacity.isalpha():
                print("Input cannot be a letter, please try again.")
            else:
                coursedata[courseid_selection]["Course Capacity"] = newcoursecapacity
                print("\nCourse Capacity Successfully Updated.\n")
                break

        #Return to menu function
        if courseedit_selection.upper() == "Q":
            print("\nReturning to Main Menu...\n")
            return

#Function for deleting courses
def deletecourse():
    #Calls menu for deletecourse
    coursedelete_menuoption = coursedeletemenu()

    #Validation for menu input
    #Making sure that its 1 or 2 as the input
    while coursedelete_menuoption != "1" and coursedelete_menuoption != "2":
        print("Input is invalid. Try again")
        coursedelete_viewcourse = input("Would you like to view courses? (Y/N): ")
        if coursedelete_viewcourse == "1" or coursedelete_viewcourse == "2":
            break

    #Scenario 1, view
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

    #Scenario 2, delete
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

        #Delete confirmation
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
    with open("cmstorage.json", "r") as file:
        dictionarydata = json.load(file)
        for key in dictionarydata:
            print("KEY:", key)
        for subkey in dictionarydata[key]:
            #Shit doesn't work yet :PPPP
            print(subkey, subkey.values())



#Menu interface
def coursemenu():
    while True:
        print(
            "---- Awesome Interface for courses!! ----\n"
            "Press 1 to add a course\n"
            "Press 2 to edit a course\n"
            "Press 3 to remove a course\n"
            "Press 4 to view existing courses\n"
            "Press 5 to return to LMS Menu\n"
        )

        viewcourse_selection = input("Choose an option: ")

        #Validation block
        while True:
            if viewcourse_selection.isalpha():
                print("Option cannot contain letters.")
                viewcourse_selection = input("Choose an option: ")
            elif viewcourse_selection == "":
                print("Option cannot be empty.")
                viewcourse_selection = input("Choose an option: ")
            elif viewcourse_selection in ("1", "2", "3", "4", "5"):
                break
            else:
                print("Invalid option")
                viewcourse_selection = input("Choose an option: ")

        #Selects a function or returns to Main Menu
        if viewcourse_selection == "1":
            addcourse()
        elif viewcourse_selection == "2":
            updatecourse()
        elif viewcourse_selection == "3":
            deletecourse()
        elif viewcourse_selection == "4":
            viewcourse()
        elif viewcourse_selection == "5":
            print("Returning to LMS Menu...")
            #Return back to LTs Main Menu
            break

coursemenu()

