#!/usr/bin/python3
#!/usr/bin/python3
import os
import string

user_file = 'users.txt'
invalid_user_chars = (" ", "|", ":")
invalid_pass_chars = (" ", "|")


def users_exists(username):
    if not os.path.exists(user_file):
        return False
    with open(user_file, 'r') as f:
        return any(line.startswith(f"{username}:") for line in f)


def valid_user(username):
    if username == "":
        print("Username cannot be empty.")
        return False
    if any(c in invalid_user_chars for c in username):
        print("Username cannot contain spaces, '|' or ':'.")
        return False
    return True


def valid_pass(password):
    if len(password) < 12:
        print("Password must be 12 characters or more.")
        return False
    if not any(c.islower() for c in password):
        print("Password should include lowercase characters.")
        return False
    if not any(c.isupper() for c in password):
        print("Password should include uppercase characters.")
        return False
    if not any(c.isdigit() for c in password):
        print("Password should include digits.")
        return False
    if not any(c in string.punctuation for c in password):
        print("Password should include special symbols.")
        return False
    if any(c in invalid_pass_chars for c in password):
        print("Password cannot contain spaces or '|'.")
        return False
    return True


def ask_new_password():
    while True:
        password = input("Enter a new password: ")
        if not valid_pass(password):
            continue
        if input("Confirm password: ") != password:
            print("Passwords do not match.")
            continue
        return password


def check_login(username, password):
    if not os.path.exists(user_file):
        return False
    with open(user_file, 'r') as f:
        return any(line.strip() == f"{username}:{password}" for line in f)


def register():
    username = input("Enter username: ").strip()
    if not valid_user(username):
        return
    if users_exists(username):
        print("User already exists.")
        return
    password = ask_new_password()
    with open(user_file, 'a') as f:
        f.write(f"{username}:{password}\n")
    print("Registration Success!")


def login():
    from main import mainmenu   # imported here to avoid a circular import
    username = input("Enter username: ").strip()
    password = input("Enter password: ")
    if check_login(username, password):
        print("Login Success!")
        mainmenu(username)
    else:
        print("Login Failed.")


def change():
    username = input("Enter username: ").strip()
    old_password = input("Enter current password: ")
    if not check_login(username, old_password):
        print("Username or password incorrect.")
        return

    new_password = ask_new_password()
    with open(user_file, 'r') as f:
        lines = f.readlines()
    with open(user_file, 'w') as f:
        for line in lines:
            if line.split(":", 1)[0] == username:
                f.write(f"{username}:{new_password}\n")
            else:
                f.write(line)
    print("Password changed!")


def loginmenu():
    options = {'1': register, '2': login, '3': change, '4': exit}
    while True:
        print("Welcome to XXXX Login Menu!")
        print("\n1. Register\n2. Login\n3. Change password\n4. Exit")
        choice = input("Choose an option: ").strip()
        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid option")


if __name__ == "__main__":
    loginmenu()