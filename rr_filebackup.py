#!/usr/bin/python3
import os
import shutil
 
 
def backup_name(txtfile):
    # resources.txt -> resources_backup.txt
    return txtfile.replace(".txt", "") + "_backup.txt"
 
 
def save(txtfile):
    #Copy the file to its backup. Call this BEFORE changing the file.
    backup = backup_name(txtfile)
    if os.path.exists(txtfile):
        shutil.copyfile(txtfile, backup)
    else:
        open(backup, "w").close()      # file didn't exist yet: backup = empty
 
 
def undo(txtfile):
    #Restore the file from its backup. Returns True if it worked.
    backup = backup_name(txtfile)
    if os.path.exists(backup):
        shutil.copyfile(backup, txtfile)
        return True
    return False

def new(txtfile):
    with open(txtfile, 'w') as file:
        file.write('Created.')

def filemenu(username):
    print("File.")
