#!/usr/bin/python3

# ---- THIS IS to read the whole file----
# with open("test1.txt", "r") as file:
#   content = file.read()
#   print(content)
#   print("\nSuccess")

# ---- THIS IS to read line by line
def read():
    file = open("test1.txt", "r")
    for line in file:
        print(line.strip())
        print("\nSuccess")
    file.close()