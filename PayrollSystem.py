import hashlib
from datetime import datetime
import pwinput

STORAGE_FORMAT = "%Y-%m-%d %H:%M:%S"

# FOR HASHING
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

# STARTING MENU
def starting():
    while True:
        print("\n--- PAYROLL SYSTEM LOGIN ---")
        print("1. Login")
        print("2. Exit")
        action = input("Enter your action: ")

        if action == "1":
            user = login()
            if user:
                menu(user)
        elif action == "2":
            print("Thank you!")
            break
        else:
            print("Invalid choice.")

# LOGIN
def login():
    username = input("Enter your username: ")
    password = pwinput.pwinput("Enter your password: ")
    hashedPassword = hashPassword(password)  # use hashPassword function

    try:
        with open("users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")  # read txt file
                if len(parts) >= 2:
                    if username == parts[0] and hashedPassword == parts[1]:  # check if parts (index) match
                        print("\nLogin success!")
                        return username

            print("Invalid username or password.")
            return None
    except FileNotFoundError:
        print("User file not found. Please register users first.")
        return None

# MAIN MENU
def menu(username):
    while True:
        print("\n======================")
        print("||  PAYROLL SYSTEM  ||")
        print("======================")
        print(f"Welcome, {username}!")
        print("\n1. Time in")
        print("2. Time out")
        print("3. Logout")

        action = input("Enter your action: ")

        if action == "1":
            record_time(username, "TIME IN")  # TIME IN tag
        elif action == "2":
            record_time(username, "TIME OUT")  # TIME OUT tag
        elif action == "3":
            print("Logging Out.")
            break
        else:
            print("Invalid option.")

# TIME IN & TIME OUT FUNCTION
def record_time(username, tag):
    now = datetime.now()  # get current time
    timestamp = now.strftime(STORAGE_FORMAT)  # format current time
    with open(f"logs_{username}.txt", "a") as f:
        f.write(f"{tag}: {timestamp}\n")  # store time to txt
    print(f"{tag} recorded: {now.strftime('%I:%M %p')}")


starting()