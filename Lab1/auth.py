import re
import json

USERS_FILE = 'storage.json'

def load_data():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": [], "projects": []}

def save_data(data):
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def register():
    data = load_data()
    users = data["users"]

    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")

    if any(u["email"] == email for u in users):
        print("Email already registered.")
        return None

    password = input("Password: ")
    confirm = input("Confirm Password: ")
    if password != confirm:
        print("Passwords do not match.")
        return None

    phone = input("Phone (Egyptian): ")
    if not re.match(r"^01[0-2,5]{1}[0-9]{8}$", phone):
        print("Invalid Egyptian phone number.")
        return None

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone": phone
    }

    users.append(user)
    save_data(data)
    print("Registered successfully!")

def login():
    data = load_data()
    email = input("Email: ")
    password = input("Password: ")

    for user in data["users"]:
        if user["email"] == email and user["password"] == password:
            print(f"Welcome, {user['first_name']}!")
            return user
    print("Invalid credentials.")
    return None

def logout():
    print("Logged out.")
