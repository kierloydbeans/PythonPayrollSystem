import hashlib
from datetime import datetime

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def starting():
    print("Welcome! What would you like to do?")
    print("1. Login")
    print("2. Exit")
    action = input("Enter your action: ")

    if action == "1":
        login()
    elif action == "2":
        print("Thank you!")
        exit()
    else:
        print("Invalid.")
        starting()

def login():
    db = open("users.txt")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashedPassword = hashPassword(password)

    try:
        with open("users.txt", "r") as f:
            for line in f:
                storedUser, storedPass = line.strip().split(",")
                if username == storedUser and hashedPassword == storedPass:
                    print("Login success!")
                    menu(username)
                    return username
        print("Invalid username or password.\n")
        starting()
        return False
    except FileNotFoundError:
        print("User does not exist.")
        return False

def menu(username):
    print("======================")
    print("||  PAYROLL SYSTEM  ||")
    print("======================")
    print("")
    print(f"Welcome {username}!")
    print("")
    print("What would you like to do?")
    print("1. Time in")
    print("2. Time out")
    print("3. Display time logs")
    print("4. Calculate salary")
    print("5. Logout")
    action = input("Enter your action: ")
    if action == "1":
        time_in(username)
    elif action == "2":
        time_out(username)
    elif action == "5":
        print(f"Logging out... Goodbye {username}!\n")
        starting()

# TIME IN FUNCTION
def time_in(username):
    now = datetime.now()
    with open(f"logs_{username}.txt", "a") as f:
        f.write(f"TIME IN: {now}\n")
    print("Time in recorded:", now)
    menu(username)


# TIME OUT FUNCTION
def time_out(username):
    now = datetime.now()
    with open(f"logs_{username}.txt", "a") as f:
        f.write(f"TIME OUT: {now}\n")
    print("Time out recorded:", now)
    menu(username)

starting()