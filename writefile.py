#!/usr/bin/python3
from readfile import *

def write():
    with open("test1.txt", "a") as file:
        file.write("\nThis is a new line!")
        with open("test1.txt", "r") as file:
            content = file.read()
            print(content)

write()