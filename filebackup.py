#!/usr/bin/python3
import shutil
import os

def save(txtfile):
    src = txtfile
    dest = txtfile - ".txt" + "_backup.txt"
    shutil.copyfile(src, dest)

def undo(txtfile):
    src = txtfile
    dest = txtfile - ".txt" + "_backup.txt"
    shutil.copyfile(dest, src)

def delete(txtfile):
    filename = input("Enter the filename: ")
    confirm = input(f"Delete {filename}? (yes / no) : ")
    while confirm not in ("Yes", "yes", "No", "no", "Quit", "quit", "q"):
        print("Please confirm.")
        confirm = input(f"Delete {filename}? (yes / no) : ")
    if confirm in ("Yes", "yes"):
        os.remove(txtfile)
        print(f"{txtfile} deleted.")
    elif confirm in ("No", "no"):
        print("Cancelled.")
        break
    elif confirm in ("Quit", "quit", "q"):
        print("Exited.")
        break

def new(txtfile):



