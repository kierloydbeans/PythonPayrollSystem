
import hashlib

def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def addUser():
    while True:
        username = input("Enter your username: ")
        while True:
            password = input("Enter your password: ")
            if len(password) < 8:
                print("Password is too short.")
            else:
                hashedPassword = hashPassword(password)
                confirmPassword = input("Confirm your password: ")
                if password != confirmPassword:
                    print("Passwords doesnt match.")
                else:
                    rateInput = input("Enter the rate of the employee: ")
                    if not rateInput.isdigit():
                        print("Numbers only.")
                    rate = int(rateInput)
                    # saving to txt
                    with open("users.txt", "a") as f:
                        f.write(f"{username},{hashedPassword}, {rate}\n")
                    print("Registration successful!")

                    # repeat
                    repeat = input("Do you want to add another? Press 'q' to quit: ")
                    if repeat.lower() == "q":
                        menu()
                    elif repeat.lower() == "y":
                        addUser()
            break
        break

def editRate():
    while True:
        print("Edit the rate of the employee")
        with open("users.txt", "r") as file:  # display current users
            lines = file.readlines()

        if not lines:
            print("No users registered.")
            break

        print("Current employees: ")
        for index, line in enumerate (lines, start=1):
            userData = line.strip().split(",")
            username = userData[0]
            rate = userData[2]
            print(f"{index}. {username}, {rate}")
        choice = input("Choose the employee number. Press 'q' to quit. ")
        if choice.lower() == 'q':
            menu()

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(lines):
                userData = lines[idx].strip().split(",")
                targetUsername = userData[0]
                newRate = input(f"Enter the new rate for {targetUsername}: ")

                if len(userData) >= 3:
                    userData[2] = f"{newRate}"
                else:
                    userData.append(f"{newRate}")
                lines[idx] = ",".join(userData) + "\n"
                with open("users.txt", "w") as file:
                    file.writelines(lines)

                print(f"Rate for {targetUsername} updated to {newRate}")

def removeUser():
    while True:
        print("Remove an employee.")
        with open("users.txt", "r") as file:
            lines = file.readlines()

        if not lines:
            print("No users registered.")
            break

        print("Current employees: ")
        for index, line in enumerate(lines, start=1):
            userData = line.strip().split(",")
            username = userData[0]
            rate = userData[2]
            print(f"{index}. {username}, {rate}")
        choice = input("Choose the employee number. Press 'q' to quit. ")

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(lines):
                userData = lines[idx].strip().split(",")
                targetUsername = userData[0]
                removedLine = lines.pop(idx)
                with open("users.txt", "w") as file:
                    file.writelines(lines)

                print(f"Employee {targetUsername} removed.")
        elif choice.lower() == "q":
            menu()
def menu():
    while True:
        print("Menu")
        print("1. Add User")
        print("2. Edit Rate")
        print("3. Remove User")
        print("3. Exit")
        action = input("Enter action: ")
        while True:
            if action == "1":
                addUser()
            elif action == "2":
                editRate()
            elif action == "3":
                removeUser()
            elif action == "4":
                exit()
            else:
                print("Invalid.")

menu()
