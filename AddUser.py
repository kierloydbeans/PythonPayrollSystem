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
                    with open("users.txt", "a") as f:
                        f.write(f"{username},{hashedPassword}\n")
                    print("Registration successful!")
            break
        break
addUser()