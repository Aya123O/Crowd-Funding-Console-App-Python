import json
from datetime import datetime

DATA_FILE = 'storage.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"users": [], "projects": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def create_project(user):
    title = input("Project Title: ")
    details = input("Details: ")
    target = input("Target Amount (EGP): ")

    start_date = input("Start Date (YYYY-MM-DD): ")
    end_date = input("End Date (YYYY-MM-DD): ")
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if end <= start:
            print("End date must be after start date.")
            return
    except ValueError:
        print("Invalid date format.")
        return

    data = load_data()
    project = {
        "title": title,
        "details": details,
        "target": target,
        "start_date": start_date,
        "end_date": end_date,
        "owner": user["email"]
    }

    data["projects"].append(project)
    save_data(data)
    print("Project created.")

def view_projects():
    data = load_data()
    for p in data["projects"]:
        print("-" * 30)
        print(f"Title: {p['title']}\nDetails: {p['details']}\nTarget: {p['target']}")
        print(f"Start: {p['start_date']} | End: {p['end_date']}\nOwner: {p['owner']}")

def edit_project(user):
    data = load_data()
    title = input("Enter the title of the project to edit: ")
    for p in data["projects"]:
        if p["title"] == title and p["owner"] == user["email"]:
            p["details"] = input("New Details: ")
            save_data(data)
            print("Project updated.")
            return
    print("Project not found or not yours.")

def delete_project(user):
    data = load_data()
    title = input("Title of project to delete: ")
    for p in data["projects"]:
        if p["title"] == title and p["owner"] == user["email"]:
            data["projects"].remove(p)
            save_data(data)
            print("Deleted.")
            return
    print("Project not found or not yours.")

def search_by_date():
    date = input("Enter a date (YYYY-MM-DD): ")
    try:
        d = datetime.strptime(date, "%Y-%m-%d")
        data = load_data()
        found = False
        for p in data["projects"]:
            start = datetime.strptime(p["start_date"], "%Y-%m-%d")
            end = datetime.strptime(p["end_date"], "%Y-%m-%d")
            if start <= d <= end:
                found = True
                print(f"- {p['title']} | {p['start_date']} - {p['end_date']}")
        if not found:
            print("No projects in that date range.")
    except ValueError:
        print("Invalid date format.")
