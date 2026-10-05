#!/usr/bin/python3
from readfile import *

def delete():
    with open("test1.txt", "r+") as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        file.writelines(lines[:-1])

delete()
read()