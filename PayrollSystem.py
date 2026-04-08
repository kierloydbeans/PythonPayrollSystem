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
    # db = open("users.txt")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashedPassword = hashPassword(password)

    try:
        with open("users.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) >= 2:
                    storedUser = parts[0]
                    storedPass = parts[1]
                    if username == storedUser and hashedPassword == storedPass:
                        print("Login success!")
                        menu(username)
                        return
                    else:
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
    elif action == "4":
        calculate_salary(username)
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

def calculate_salary(username):
    total_hours = 0
    time_in_val = None
    rate = 0.0

# get rate
    try:
        with open(f"users.txt","r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts[0] == username:
                    rate = float(parts[2]) if len(parts) > 2 else 0.0
                    break
    except (FileNotFoundError, ValueError):
        rate = 0.0

# computation
    try:
        with open(f"logs_{username}.txt", "r") as file:
            for line in file:
                if ": " in line:
                    tag, timestamp_str = line.strip()   .split(": ", 1)
                    t_obj = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")

                    if tag == "TIME IN":
                        time_in_val = t_obj
                    elif tag == "TIME OUT" and time_in_val:
                        duration = t_obj - time_in_val
                        total_hours += duration.total_seconds() / 3600
                        time_in_val = None

        salary = total_hours * rate
        print("-"*30)
        print(f"Total Hours: {total_hours:.2f}")
        print(f"Hourly Rate: ₱{rate:.2f}")
        print(f"GROSS PAY: ₱{salary:.2f}")
        print("-" * 30)
    except FileNotFoundError:
        print("No logs found for the user.")

    input("\n Press Enter to return to home")
    menu(username)
starting()