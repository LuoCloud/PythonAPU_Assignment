#Adding courses (Ask for module, course, etc.)
#Suggested fields: Course ID, Course Name, Instructor, Duration, Fee, Maximum Capacity.

#Updating existing courses (be able to update the
#database file

#Delete feature that removes the data from the
#database file

#Master dictionary for courses
coursedata = {}

#Function for adding courses
def addcourse():
    courseamount = int(input("How many courses would you like to add?: "))
    if courseamount < 0:
        print("Course amount cannot be negative.")
        courseamount = int(input("How many courses would you like to add?: "))
    elif courseamount >= 1:
        pass
    elif courseamount > 3:
        print("Please add a few courses at a time.")
        courseamount = int(input("How many courses would you like to add?: "))
    else:
        print("Value is invalid.")
        courseamount = int(input("How many courses would you like to add?: "))


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

        courseamount -= 1
        print("Provide details for the next course.")
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

#Function for viewing courses
def viewcourse():
    print(coursedata)

#Course edit menu for updatecourse()
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

#Function for updating courses (Needs to be able to pinpoint a field and edit it)
def updatecourse():
    courseid_selection = input("Please insert your Course ID to edit: ")
    courseedit_selection = courseeditmenu()

    #Block for course name editing
    if courseedit_selection == "1":
        newcoursename = input("New Course Name: ")

        #Validation block
        if newcoursename == "":
            print("Input is empty, please try again.")
            newcoursename = input("New Course Name: ")
        elif newcoursename.isdigit():
            print("Input cannot be a number, please try again.")
            newcoursename = input("New Course Name: ")
        else:
            coursedata[courseid_selection]["Course Name: "] = newcoursename
            print("Course Name Successfully Updated.\n")
            courseeditmenu()

    #Block for course instructor editing
    if courseedit_selection == "2":
        newcourseinstructor = input("New Course Instructor: ")

        #Validation block
        if newcourseinstructor == "":
            print("Input is empty, please try again.")
            newcourseinstructor = input("New Course Instructor: ")
        elif newcourseinstructor.isdigit():
            print("Input cannot be a number, please try again.")
            newcourseinstructor = input("New Course Instructor: ")
        else:
            coursedata[courseid_selection]["Course Instructor: "] = newcourseinstructor
            print("Course Instructor Successfully Updated.\n")
            courseeditmenu()

    #Block for course duration editing
    if courseedit_selection == "3":
        newcourseduration = input("New Course Duration: ")

        #Validation
        if newcourseduration == "":
            print("Input is empty, please try again.")
            newcourseduration = input("New Course Duration: ")
        elif newcourseduration.isdigit():
            print("Input cannot be a number, please try again.")
            newcourseduration = input("New Course Duration: ")
        else:
            coursedata[courseid_selection]["Course Duration: "] = newcourseduration
            print("Course Duration Successfully Updated.\n")
            courseeditmenu()

    #Block for course fee editing
    if courseedit_selection == "4":
        newcoursefee = input("New Course Fee: ")

        #Validation
        if newcoursefee == "":
            print("Input is empty, please try again.")
            newcoursefee = input("New Course Fee: ")
        elif newcoursefee.isalpha():
            print("Input cannot be a letter, please try again.")
            newcoursefee = input("New Course Fee: ")
        else:
            coursedata[courseid_selection]["Course Fee: "] = newcoursefee
            print("Course Fee Successfully Updated.\n")
            courseeditmenu()

    #Block for course capacity editing
    if courseedit_selection == "5":
        newcoursecapacity = input("New Course Capacity: ")
        #Validation
        if newcoursecapacity == "":
            print("Input is empty, please try again.")
            newcoursecapacity = input("New Course Capacity: ")
        elif newcoursecapacity.isalpha():
            print("Input cannot be a letter, please try again.")
            newcoursecapacity = input("New Course Capacity: ")
        else:
            coursedata[courseid_selection]["Course Capacity"] = newcoursecapacity
            print("Course Capacity Successfully Updated.\n")
            courseeditmenu()

    if courseedit_selection.upper() == "Q":
        pass #go back to course menu

#Function for deleting courses
def deletecourse():
    pass

#Menu interface
def coursemenu():
    print(
        "---- Awesome Interface for courses!! ----\n"
        "Press 1 to add a course\n"
        "Press 2 to edit a course\n"
        "Press 3 to remove a course\n"
    )
    viewcourse_selection = input("Choose an option: ")

viewcourse()


