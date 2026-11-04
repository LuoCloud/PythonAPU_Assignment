# display functions and menu prompts

def show_menu():
    print("\nenrollment system menu")
    print("1. add enrollment")
    print("2. view enrollments")
    print("3. update status")
    print("4. delete enrollment")
    print("5. back")
    print("6. view audit logs")

def display_table(records):
    print("records list:")
    for r in records:
        print(f"enrollment id: {r[0]} | member: {r[1]} | course: {r[2]} | date: {r[3]} | status: {r[4]}")

def status_menu():
    print("pick a status:")
    print("1. active")
    print("2. completed")
    print("3. withdrawn")


