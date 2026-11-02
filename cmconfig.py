#Place whatever important information or
#passwords here

def passwordcreation():
    print("Would you like to create a password?")
    passwordanswer = input("Y/N: ")
    if passwordanswer.upper() == "Y":
        print("Your password is creating")
    elif passwordanswer.upper() == "N":
        print("No Password boi")
    else:
        print("YOUUU SHALL NOT PAAAAAAAAAAAAAAAS")

passwordcreation()
