import hashlib

# FOR HASHING
def hashPassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

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
def menu():
    while True:
        print("Menu")
        print("1. Add User")
        print("2. Edit Rate")
        print("3. Remove User")
        print("4. Exit")
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
