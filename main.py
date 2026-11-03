#!/usr/bin/python3
import os

# from login import main
from member import membermenu
from course import coursemenu
from enrollment import enrollmentmenu
from resources import resourcemenu
from rr_filebackup import filemenu
from info import infomenu 

def mainmenu(username):
    print("\n----Welcome!----")
    print(f"Welcome back! {username}.")
    print("Here are some options for you: ")
    print("(m)ember | (c)ourse | (e)nrollment | (r)esource | (o)ther " )
    print("PRESS 'Q' to exit.")
    selection = input("Select: ")

    while selection not in ("q", "Q"):
        while selection not in ("m", "M", "c", "C", "e", "E", "r", "R", "o", "O", "q", "Q"):
            print("Please enter m, c, e, r, o or q.")
            selection = input("Select: ")
        if selection in ("m", "M"):
            membermenu()
            break
        elif selection in ("c", "C"):
            coursemenu()
            break
        elif selection in ("e", "E"):
            enrollmentmenu()
            break
        elif selection in ("r", "R"):
            resourcemenu(username)
            break
        elif selection in ("o", "O"):
            print("(f)ile | (i)nfo | (l)og out")
            choice = input("Select: ")
            while choice not in ("q", "Q"):
                while choice not in ("f", "F", "i", "I", "l", "L", "q", "Q"):
                    print("Please enter f, i or l.")
                    choice = input("Select: ")
                if choice in ("f", "F"):
                    filemenu(username)
                    break
                elif choice in ("i", "I"):
                    infomenu(username)
                    break
                elif choice in ("l", "L"):
                    print("Logged out.")
                    break
            break
    print("Thank you. Goodbye! (Main)")
if __name__ == "__main__":
    username = input("Username: ")
    mainmenu(username)