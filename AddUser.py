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
        choice = input("Choose the employee number. Press 'q' to quit.")
        if choice.lower() == 'q':
            break

        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(lines):
                targetLine = lines[idx].strip().split(",")
                targetUser = userData[0]
                newRate = input(f"Enter the new rate for {targetUser}: ")

                if len(targetUser) < 3:
                    userData.append(newRate)
                else:
                    userData[2] = newRate

                lines[idx] = ",".join(userData) + "\n"

                with open("users.txt", "w") as file:
                    file.writelines(lines)

                print(f"Rate for {targetUser} updated to {newRate}")

def menu():
    while True:
        print("Menu")
        print("1. Add User")
        print("2. Edit Rate")
        action = input("Enter action: ")
        while True:
            if action == "1":
                addUser()
            elif action == "2":
                editRate()
            else:
                print("Invalid.")

menu()