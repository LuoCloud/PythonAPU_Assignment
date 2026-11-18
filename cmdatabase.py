# This file contains loading and saving functions to the database, as well as an extra function.
# Database for CMS

# Course Loading Function
def load_coursedata():
    #Checking if there is course in storage and loading if available
    coursedata = {}
    try:
        with open("cmstorage.txt", "r") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) < 6:
                    continue
                coursedata[parts[0]] = {
                    "courname": parts[1],
                    "courinstructor": parts[2],
                    "courduration": parts[3],
                    "courfee": parts[4],
                    "courcapacity": parts[5]
                }
    except Exception as e:
        print(e)
        coursedata = {}
    return coursedata

# Course Saving Function
def save_coursedata(coursedata):
    try:
        with open("cmstorage.txt", "w") as file:
            for courid, details in coursedata.items():
                line = f"{courid}|{details['courname']}|{details['courinstructor']}|{details['courduration']}|{details['courfee']}|{details['courcapacity']}\n"
                file.write(line)
        print("\nCourse stored.")
    except Exception as e:
        print("Failed to process file:", e)

# Function for limiting course amount
def extra_maximumcourse(courseamount):
    try:
        with open("cmstorage.txt", "r") as file:
            extra_courseamount = len(file.readlines())

        totalcourseamount = courseamount + extra_courseamount

        if totalcourseamount > 20:
            print("Course limit reached, 20\n"
                  f"Current course amount {extra_courseamount}\n"
                  f"You wanted to add {courseamount}\n")
            return "Limit reached"
        else:
            return "Limit not reached"
    except:
        pass
