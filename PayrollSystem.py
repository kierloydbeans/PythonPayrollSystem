import hashlib


def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashedPassword = hashPassword(password)

    try:
        with open("users.txt", "r") as f:
            for line in f:
                storedUser, storedPass = line.strip().split(",")
                if username == storedUser and hashedPassword == storedPass:
                    print("Login success!")
                    menu(username)  # <--- Change this line to include 'username'
                    return username
        print("Invalid username or password")
        return False
    except FileNotFoundError:
        print("User does not exist.")
        return False

def menu(username):
    print(f"Welcome {username}!")

login()