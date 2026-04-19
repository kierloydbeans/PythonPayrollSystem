import hashlib
import datetime
import shutil
import os
import pwinput

STORAGE_FORMAT = "%Y-%m-%d %H:%M:%S"

# FOR HASHING
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login():
    # db = open("users.txt")
    username = input("Enter your username: ")
    password = pwinput.pwinput("Enter your password: ")
    hashedPassword = hashPassword(password)  # use hashPassword function

    try:
        with open("admins.txt", "r") as f:
            for line in f:
                parts = line.strip().split(",")  # read txt file
                if len(parts) >= 2:
                    if username == parts[0] and hashedPassword == parts[1]:  # check if parts (index) match
                        print("\nLogin success!")
                        menu()
                        return username

            print("Invalid username or password.")
            return None
    except FileNotFoundError:
        print("User file not found. Please register users first.")
        return None

# ADDING USER
def addUser():
    while True:
        username = input("Enter your username: ")
        while True:
            password = input("Enter your password: ")
            # check if password is long enough
            if len(password) < 8:
                print("Password is too short.")
            else:
                # hash the pw
                hashedPassword = hashPassword(password)
                # confirm if pw match
                confirmPassword = input("Confirm your password: ")
                if password != confirmPassword:
                    print("Passwords doesnt match.")
                else:
                    rateInput = input("Enter the rate of the employee: ")
                    # check if input is digit
                    if not rateInput.isdigit():
                        print("Numbers only.")
                    # convert to int for calculation
                    rate = int(rateInput)
                    # saving to txt, using append to not overwrite the old content of txt file
                    with open("users.txt", "a") as f:
                        f.write(f"{username},{hashedPassword}, {rate}\n")
                    print("Registration successful!")
                    # repeat
                    repeat = input("Do you want to add another? Press 'q' to quit: ")
                    if repeat.lower() == "q":
                        menu()  # back to menu
                    elif repeat.lower() == "y":
                        addUser()  # add another user
            break
        break

# EDIT USER RATES
def editRate():
    while True:
        print("Edit the rate of the employee")
        with open("users.txt", "r") as file:  # display current users
            lines = file.readlines()
        if not lines:
            print("No users registered.")
            input("\n Press any key to continue.\n")
            menu()

        print("Current employees: ")
        # printing of users.txt content
            # set index                      index starts with 1
        for index, line in enumerate (lines, start=1):
            userData = line.strip().split(",")
            username = userData[0]  # 0 is index of  username
            rate = userData[2]  # 2 is index of rate
            print(f"{index}. {username}, {rate}")  # ex: index is 1. username is kier. rate is 500
        choice = input("Choose the employee number. Press 'q' to quit. ")
        if choice.lower() == 'q':
            menu()  # back to menu

        if choice.isdigit():
            idx = int(choice) - 1  # -1 because our index before started with 1
            if 0 <= idx < len(lines):  # check if the index is less than the length of the txt contents and not less than 0
                userData = lines[idx].strip().split(",")
                targetUsername = userData[0]  # gets the username (index 0)
                newRate = input(f"Enter the new rate for {targetUsername}: ")

                if len(userData) >= 3:  # 0 1 2 only. 3 or more means rate alr exists
                    userData[2] = f"{newRate}"  # replace the old rate (index 2)
                else:
                    userData.append(f"{newRate}")  # if no rate yet (less than 3 index), append
                lines[idx] = ",".join(userData) + "\n"  # combine all index together again for storing
                with open("users.txt", "w") as file:
                    file.writelines(lines)  # overwrite the current rate (index 2)

                print(f"Rate for {targetUsername} updated to {newRate}")

def removeUser():
    while True:
        print("Remove an employee.")
        with open("users.txt", "r") as file:
            lines = file.readlines()  # display the users

        if not lines:
            print("No users registered.")
            input("\nPress any key to continue.\n")
            menu()

        print("Current employees: ")  # printing current users; same as edit
        for index, line in enumerate(lines, start=1):
            userData = line.strip().split(",")
            username = userData[0]
            rate = userData[2]
            print(f"{index}. {username}, {rate}")
        choice = input("Choose the employee number. Press 'q' to quit. ")

        if choice.isdigit():
            idx = int(choice) - 1  # -1 because we started with index 1
            if 0 <= idx < len(lines):
                userData = lines[idx].strip().split(",")
                targetUsername = userData[0]  # username index
                removedLine = lines.pop(idx)  # line to remove
                with open("users.txt", "w") as file:
                    file.writelines(lines)  # overwrite the line with a pop

                print(f"Employee {targetUsername} removed.")
        elif choice.lower() == "q":
            menu()

# TIME LOGS
def display_time_logs(username):
    print(f"\n--- LOG HISTORY FOR {username.upper()} ---")
    print(f"{'DATE':<12} | {'TIME IN':<12} | {'TIME OUT':<12}")
    print("-" * 45)

    log_file = f"logs_{username}.txt"  # check the txt file depending on username
    if not os.path.exists(log_file):  # check if it exists
        print("No logs found.")
        return

    with open(log_file, "r") as file:
        time_in_val = None  # initialize empty variable
        found = False  # initialize empty variable
        for line in file:
            if ": " in line:
                tag, timestamp_str = line.strip().split(": ", 1)  # split the content on the first ":"
                t_obj = datetime.datetime.strptime(timestamp_str, STORAGE_FORMAT)  # converts string to datetime

                if tag == "TIME IN":
                    time_in_val = t_obj  # dont display yet if no time out
                elif tag == "TIME OUT" and time_in_val:  # display if both exists
                    print(f"{time_in_val.strftime('%Y-%m-%d'):<12} | "
                          f"{time_in_val.strftime('%I:%M %p'):<12} | "
                          f"{t_obj.strftime('%I:%M %p'):<12}")
                    time_in_val = None  # set back to none
                    found = True

        if not found:
            print("No completed shifts recorded.")

    input("\nPress Enter to return...")


def menu():
    while True:
        print("\n" + "=" * 30)
        print("      PAYROLL SYSTEM")
        print("=" * 30)
        print("1. Add User")
        print("2. Edit Rate")
        print("3. Remove User")
        print("4. Record of Employee")
        print("5. View User Logs")
        print("6. Request Payslip")
        print("7. Generate Payroll Report")
        print("8. Export Payslip to CSV")
        print("9. Logout")

        action = input("Enter action: ")

        if action == "1":
            addUser()
        elif action == "2":
            editRate()
        elif action == "3":
            removeUser()
        elif action == "4":
            recordOfEmployee()
        elif action == "5":
            target = input("Enter username: ")
            display_time_logs(target)
        elif action == "6":
            target = input("Enter username: ")
            calculate_salary(target)
        elif action == "7":
            generateReportOfPayroll()
        elif action == "8":
            target = input("Enter username: ")
            exportToCSV(target)
        elif action == "9":
            starting()
        else:
            print("Invalid selection. Try again.")

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
            exit()
        else:
            print("Invalid choice.")
def listOfUsers():
    logFile = f"users.txt"

    # open file
    with open(f"users.txt", "r") as file:
        # printing
        for line in file:
                print(line.strip())


def recordOfEmployee():
    print("\n--- VIEW EMPLOYEE RECORD ---")
    with open("users.txt", "r") as file:
        lines = file.readlines()

    if not lines:
        print("No employees found.")
        return

    for index, line in enumerate(lines, start=1):
        data = line.strip().split(",")
        if len(data) >= 1:
            print(f"{index}. {data[0]}")

    choice = input("\nSelect employee number to view record (or 'q' to quit): ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(lines):
            target_user = lines[idx].strip().split(",")[0]
            display_time_logs(target_user)
            calculate_salary(target_user)
    elif choice.lower() == 'q':
        menu()


def generateReportOfPayroll():
    print("\n" + "=" * 40)
    print(f"{'NAME':<15} | {'HOURLY RATE':<12} | {'GROSS PAY'}")
    print("-" * 40)

    try:
        with open("users.txt", "r") as file:
            for line in file:
                userData = line.strip().split(",")
                if len(userData) >= 3:
                    username = userData[0]
                    rate = float(userData[2].strip())
                    total_hours = 0
                    time_in_val = None
                    log_file = f"logs_{username}.txt"
                    if os.path.exists(log_file):
                        with open(log_file, "r") as f_logs:
                            for log_line in f_logs:
                                if ": " in log_line:
                                    tag, timestamp_str = log_line.strip().split(": ", 1)
                                    try:
                                        t_obj = datetime.datetime.strptime(timestamp_str, STORAGE_FORMAT)
                                        if tag == "TIME IN":
                                            time_in_val = t_obj
                                        elif tag == "TIME OUT" and time_in_val:
                                            duration = t_obj - time_in_val
                                            total_hours += duration.total_seconds() / 3600
                                            time_in_val = None
                                    except ValueError:
                                        continue
                    gross_pay = total_hours * rate
                    print(f"{username:<15} | ₱{userData[2]:<11} | {gross_pay:.2f}")
    except FileNotFoundError:
        print("Users database not found.")

    print("=" * 40)
    if input("\nPress Enter to return to menu...") == "":
        menu()


def calculate_salary(username):
    total_hours = 0
    time_in_val = None
    rate = 0.0

    try:
        with open("users.txt", "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts[0] == username and len(parts) >= 3:
                    rate = float(parts[2].strip())
                    break
    except FileNotFoundError:
        print("Error: users.txt not found.")
        return

    log_file = f"logs_{username}.txt"
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            for line in file:
                if ": " in line:
                    tag, timestamp_str = line.strip().split(": ", 1)
                    try:
                        t_obj = datetime.datetime.strptime(timestamp_str, STORAGE_FORMAT)

                        if tag == "TIME IN":
                            time_in_val = t_obj
                        elif tag == "TIME OUT" and time_in_val:
                            duration = t_obj - time_in_val
                            total_hours += duration.total_seconds() / 3600
                            time_in_val = None
                    except ValueError:
                        continue
    else:
        print(f"No logs found for {username}.")

    salary = total_hours * rate

    print("\n" + "-" * 30)
    print(f"SALARY SUMMARY: {username.upper()}")
    print(f"Total Hours:  {total_hours:.2f}")
    print(f"Hourly Rate:  ₱{rate:.2f}")
    print(f"GROSS PAY:    ₱{salary:.2f}")
    print("-" * 30)
    if input("\nPress Enter to return to menu...") == "":
        menu()

def filterLogs(username, tag):
    # file
    logFile = f"logs_{username}.txt"

    # open file
    with open(f"logs_{username}.txt", "r") as file:
    # printing
        for line in file:
            if line.startswith(tag):
                print(line.strip())

def exportToCSV(username):
    source = f"logs_{username}.txt"
    destination = f"reports_{username}.csv"
    shutil.copyfile(source, destination)
    print(f"Exported to {destination}")


starting()