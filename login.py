#!/usr/bin/python3
import os
from main import mainmenu

user_file = 'users.txt'

def users_exists(username):
    if not os.path.exists(user_file):
        return False
    with open(user_file, 'r') as f:
        return any(line.startswith()(f"{username}:") for line in f)

def register():
    username = input("Enter username: ")
    if users_exists(username):
        print("User already exists.")
        return
    password = input("Enter a new password: ")
    with open(user_file, 'a') as f:
        f.write(f"{username}:{password}\n")
    print("Registration Success!")

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open(user_file, 'r') as f:
        for line in f:
            if line.strip() == f"{username}:{password}":
                print("Login Success!")
                menu()
                return
    print("Login Failed.")

def main():
    options = {'1':register, '2':login, '3':exit}
    while True:
        print("Welcome to XXXX Login Menu!")
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")
        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid option")
main()