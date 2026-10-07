#!/usr/bin/python3
from filebackup import *

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
