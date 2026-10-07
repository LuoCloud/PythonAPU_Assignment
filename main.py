#!/usr/bin/python3
from resources import *
from filebackup import *

user = ""

print("----Welcome!----")

user = input("Username : ")
while not user.isalpha():
    print("Username invalid! Please try again.")
    user = input("Username : ")

print("Username valid!")
password = input("Password : ")
while not password.isdigit():
    print("Password invalid! Digits only, please.")
    password = input("Password : ")

print("Login successful!")
print(f"Welcome back! {user}.")
print("Here are some options for you: ")
print("(m)embers  (c)ourses  (e)nrollments  (r)esources  (q)uit" )
selection = input("Select: ")

while selection not in ("q", "Q"):
    while selection not in ("m", "M", "c", "C", "e", "E", "r", "R", "q", "Q"):
        print("Please enter m, c, e, r or q.")
        selection = input("Select: ")
    if selection in ("q", "Q"):
        print("Thank you. Goodbye!")
        break
print("Thank you. Goodbye!")