#!/usr/bin/python3
import os

from member import membermenu
from course import coursemenu
from enrollment import enrollmentmenu
from resources import resourcemenu, filtering
from rr_filebackup import filemenu

def infomenu(username):
    print("-------")
    print("--Roles Assign--")
    print("Mandatory Functions:")
    print("Wong Li Ting TP174742: Resources, Main Menu")
    print("Chin Jun Xiang TPXXXXXX: Member, Main Menu")
    print("Lee Jun Xuan TPXXXXXX: Course")
    print("Yap Kai Bin TPXXXXXX: Enrollment")
    print("---")
    print("Additional Functions:")
    print("Wong Li Ting TP174742: Login Menu, Filtering/Searching")
    print("Chin Jun Xiang TPXXXXXX: Login Menu, Auto-generated ID")
    print("Lee Jun Xuan TPXXXXXX: Course Capacity Check")
    print("Yap Kai Bin TPXXXXXX: Text-file log of daily operations")
    print("-------")
    print("To be continued.....(Ask lecturer)")

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
            membermenu(username)
            mainmenu(username)
            break
        elif selection in ("c", "C"):
            coursemenu(username)
            mainmenu(username)
            break
        elif selection in ("e", "E"):
            enrollmentmenu(username)
            mainmenu(username)
            break
        elif selection in ("r", "R"):
            resourcemenu(username)
            mainmenu(username)
            break
        elif selection in ("o", "O"):
            print("(f)ilter | (i)nfo | (l)og out")
            choice = input("Select: ")
            while choice not in ("q", "Q"):
                while choice not in ("f", "F", "i", "I", "l", "L", "q", "Q"):
                    print("Please enter f, i or l.")
                    choice = input("Select: ")
                if choice in ("f", "F"):
                    filtering(username)
                    mainmenu(username)
                    return
                elif choice in ("i", "I"):
                    infomenu(username)
                    mainmenu(username)
                    break
                elif choice in ("l", "L"):
                    from login import loginmenu
                    loginmenu()
                    break
            break
    print("Thank you. Goodbye! (Main)")

if __name__ == "__main__":
    from login import loginmenu
    loginmenu()
