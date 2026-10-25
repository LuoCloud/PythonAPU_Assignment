#!/usr/bin/python3
from rr_filebackup import *

test = 1
# ---- THIS IS to read the whole file----
# with open("test1.txt", "r") as file:
#   content = file.read()
#   print(content)
#   print("\nSuccess")

# ---- THIS IS to read line by line
def readline():
    file = open("test1.txt", "r")
    for line in file:
        print(line.strip())
        print("\nSuccess")
    file.close()

def writeline():
    with open("test1.txt", "a") as file:
        file.write("\nThis is a new line!")
        with open("test1.txt", "r") as file:
            content = file.read()
            print(content)

def deleteline():
    with open("test1.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        file.writelines(lines[:-1])

def deletespecify():
    name = input("What to delete? : ")
    with open("text1.txt", "r") as file:
        lines = file.readlines()
    with open("text1.txt", "w") as file:
        for line in lines:
            if (line.strip("\n") != name):
                file.write(line)

def resources():
    # Show the total line of the resources data
    # Show 5 categories of resources
    print("---Resources---")
    print("| ID | NAME | CATEGORY | QUANTITY | STATUS |")
    print(f"{user}, ")
    # Ask which category user wants to look at
    if test == 1:
        print(f"You don't have access to read or edit.")
        choice = input("Do you want to quit?")
        while choice not in ("y", "Y", "yes", "Yes", "YES"):
            print("Command accepted.")
            print(f"{user}, ")
            print(f"You don't have access to read or edit.")
            choice = input("Do you want to quit?")
    # check user's access by using dict or file
    else:
        # -- if user in admindata.txt, then they're allow to execute other than READ
        # What do the user wants to do
        print("Please enter...")
        choice = input("(r)ead, (e)dit, (d)elete, (c)hange, (q)uit : ")
        # Jump to the files
        while choice not in ("q", "Q"):
            while choice not in ("r", "R", "e", "E", "d", "D", "c", "C"):
                choice = input("Please enter (r)ead, (e)dit, (d)elete, (c)hange, (q)uit : ")
            if choice in ("r", "R"):
                read()
            if choice in ("e", "E"):
                readline()
            if choice in ("d", "D"):
                readline()
            if choice in ("c", "C"):
                readline()
    print("Program executed.")
    resources()