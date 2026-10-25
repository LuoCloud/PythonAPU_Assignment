#!/usr/bin/python3
from resources import resources

def menu():
    print("----Welcome!----")

    print(f"Welcome back! {username}.")
    print("Here are some options for you: ")
    print("(m)embers  (c)ourses  (e)nrollments  (r)esources  (q)uit" )
    selection = input("Select: ")

    while selection not in ("q", "Q"):
        while selection not in ("m", "M", "c", "C", "e", "E", "r", "R", "q", "Q"):
            print("Please enter m, c, e, r or q.")
            selection = input("Select: ")
        # if selection in ("m", "M"):
        # if selection in ("c", "C"):
        # if selection in ("e", "E"):
        if selection in ("r", "R"):
            resources()
    print("Thank you. Goodbye!")