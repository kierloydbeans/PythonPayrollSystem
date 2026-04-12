import hashlib
from datetime import datetime
import os

STORAGE_FORMAT = "%Y-%m-%d %H:%M:%S"


def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()


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
                    if username == parts[0] and hashedPassword == parts[1]:
                        print("\nLogin success!")
                        return username

            print("Invalid username or password.")
            return None
    except FileNotFoundError:
        print("User file not found. Please register users first.")
        return None


def menu(username):
    while True:
        print("\n======================")
        print("||  PAYROLL SYSTEM  ||")
        print("======================")
        print(f"Welcome, {username}!")
        print("\n1. Time in")
        print("2. Time out")
        print("3. Display daily time logs")
        print("4. Calculate salary")
        print("5. Logout")

        action = input("Enter your action: ")

        if action == "1":
            record_time(username, "TIME IN")
        elif action == "2":
            record_time(username, "TIME OUT")
        elif action == "3":
            display_time_logs(username)
        elif action == "4":
            calculate_salary(username)
        elif action == "5":
            print(f"Logging out... Goodbye {username}!")
            break
        else:
            print("Invalid option.")

# TIME IN & TIME OUT FUNCTION
def record_time(username, tag):
    now = datetime.now()
    timestamp = now.strftime(STORAGE_FORMAT)
    with open(f"logs_{username}.txt", "a") as f:
        f.write(f"{tag}: {timestamp}\n")
    print(f"{tag} recorded: {now.strftime('%I:%M %p')}")

# time logs
def display_time_logs(username):
    print(f"\n--- LOG HISTORY FOR {username.upper()} ---")
    print(f"{'DATE':<12} | {'TIME IN':<12} | {'TIME OUT':<12}")
    print("-" * 45)

    log_file = f"logs_{username}.txt"
    if not os.path.exists(log_file):
        print("No logs found.")
        return

    with open(log_file, "r") as file:
        time_in_val = None
        found = False
        for line in file:
            if ": " in line:
                tag, timestamp_str = line.strip().split(": ", 1)
                t_obj = datetime.strptime(timestamp_str, STORAGE_FORMAT)

                if tag == "TIME IN":
                    time_in_val = t_obj
                elif tag == "TIME OUT" and time_in_val:
                    print(f"{time_in_val.strftime('%Y-%m-%d'):<12} | "
                          f"{time_in_val.strftime('%I:%M %p'):<12} | "
                          f"{t_obj.strftime('%I:%M %p'):<12}")
                    time_in_val = None
                    found = True

        if not found:
            print("No completed shifts recorded.")

    input("\nPress Enter to return...")


def calculate_salary(username):
    total_hours = 0
    time_in_val = None
    rate = 0.0

    # get rate
    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts[0] == username:
                    rate = float(parts[2]) if len(parts) > 2 else 0.0
                    break
    except:
        rate = 0.0

    # compute hours
    log_file = f"logs_{username}.txt"
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            for line in file:
                if ": " in line:
                    tag, timestamp_str = line.strip().split(": ", 1)
                    t_obj = datetime.strptime(timestamp_str, STORAGE_FORMAT)

                    if tag == "TIME IN":
                        time_in_val = t_obj
                    elif tag == "TIME OUT" and time_in_val:
                        duration = t_obj - time_in_val
                        total_hours += duration.total_seconds() / 3600
                        time_in_val = None

    salary = total_hours * rate
    print("\n" + "-" * 30)
    print(f"SALARY SUMMARY")
    print(f"Total Hours:  {total_hours:.2f}")
    print(f"Hourly Rate:  ₱{rate:.2f}")
    print(f"GROSS PAY:    ₱{salary:.2f}")
    print("-" * 30)
    input("\nPress Enter to return...")

starting()