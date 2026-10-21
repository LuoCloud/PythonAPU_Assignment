#Adding courses (Ask for module, course, etc.)
#Suggested fields: Course ID, Course Name, Instructor, Duration, Fee, Maximum Capacity.

#Updating existing courses (be able to update the
#database file

#Delete feature that removes the data from the
#database file

def addcourse():
    courseamount = int(input("How many courses would you like to add?: "))
    if courseamount < 0:
        print("Course amount cannot be negative.")
        courseamount = int(input("How many courses would you like to add?: "))
    elif courseamount > 3:
        print("Please add a few courses at a time.")
        courseamount = int(input("How many courses would you like to add?: "))
    else:
        print("Value is invalid.")
        courseamount = int(input("How many courses would you like to add?: "))

courses = {}

#Important to note that courseid serves as the unique key in the dictionary
#While others will be the values to the key (courseid)
courseid = str(input("Course ID (e.g. (092026-MAL)): "))
if courseid == "":
    print("Provide a valid course ID.")
elif courseid in courses:
    print("Course already exists")
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

courseinputs = dict(coursename : [courseid, courseinstructor, coursedur, coursefee, coursecap])
Update(courses[courseinputs])


