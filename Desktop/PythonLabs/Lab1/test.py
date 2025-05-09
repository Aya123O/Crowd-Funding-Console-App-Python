import re
import json
import datetime
from getpass import getpass

# Data storage
users = []
projects = []
logged_in_user = None

# File paths
USERS_FILE = "users.json"
PROJECTS_FILE = "projects.json"

def load_data():
    global users, projects
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []
    
    try:
        with open(PROJECTS_FILE, 'r') as f:
            projects = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        projects = []

def save_data():
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    with open(PROJECTS_FILE, 'w') as f:
        json.dump(projects, f)

def validate_egyptian_phone(number):
    # Egyptian phone number regex (starts with 01 and has 11 digits)
    pattern = r'^01[0-2,5]{1}[0-9]{8}$'
    return re.match(pattern, number) is not None

def validate_email(email):
    # Simple email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register():
    print("\n--- Registration ---")
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    
    while True:
        email = input("Email: ").strip()
        if not validate_email(email):
            print("Invalid email format. Please try again.")
            continue
        
        if any(user['email'] == email for user in users):
            print("Email already exists. Please use another email.")
        else:
            break
    
    while True:
        password = getpass("Password: ").strip()
        confirm_password = getpass("Confirm Password: ").strip()
        if password != confirm_password:
            print("Passwords don't match. Please try again.")
        else:
            break
    
    while True:
        mobile = input("Mobile Phone (Egyptian number): ").strip()
        if validate_egyptian_phone(mobile):
            break
        else:
            print("Invalid Egyptian phone number. It should start with 01 and have 11 digits.")
    
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,  # Note: In a real app, store hashed passwords
        'mobile': mobile,
        'active': True  # Assuming immediate activation for simplicity
    }
    
    users.append(user)
    save_data()
    print("\nRegistration successful! You can now login.")

def login():
    global logged_in_user
    print("\n--- Login ---")
    email = input("Email: ").strip()
    password = getpass("Password: ").strip()
    
    for user in users:
        if user['email'] == email and user['password'] == password:
            if user.get('active', True):  # Check if account is active
                logged_in_user = user
                print(f"\nWelcome back, {user['first_name']}!")
                return
            else:
                print("\nAccount not activated. Please check your email for activation.")
                return
    
    print("\nInvalid email or password.")

def create_project():
    print("\n--- Create Project ---")
    title = input("Project Title: ").strip()
    details = input("Project Details: ").strip()
    
    while True:
        try:
            target = float(input("Total Target (EGP): ").strip())
            if target <= 0:
                print("Target must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    while True:
        start_date = input("Start Date (YYYY-MM-DD): ").strip()
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    while True:
        end_date = input("End Date (YYYY-MM-DD): ").strip()
        try:
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            if end_date <= start_date:
                print("End date must be after start date.")
                continue
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    
    project = {
        'title': title,
        'details': details,
        'target': target,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
        'owner_email': logged_in_user['email'],
        'created_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    projects.append(project)
    save_data()
    print("\nProject created successfully!")

def view_projects(filter_func=None):
    print("\n--- All Projects ---")
    projects_to_display = projects if filter_func is None else filter_func(projects)
    
    if not projects_to_display:
        print("No projects found.")
        return
    
    for idx, project in enumerate(projects_to_display, 1):
        print(f"\nProject #{idx}")
        print(f"Title: {project['title']}")
        print(f"Details: {project['details']}")
        print(f"Target: {project['target']} EGP")
        print(f"Start Date: {project['start_date']}")
        print(f"End Date: {project['end_date']}")
        print(f"Created by: {project['owner_email']}")

def edit_project():
    user_projects = [p for p in projects if p['owner_email'] == logged_in_user['email']]
    
    if not user_projects:
        print("\nYou don't have any projects to edit.")
        return
    
    print("\n--- Your Projects ---")
    for idx, project in enumerate(user_projects, 1):
        print(f"{idx}. {project['title']} (Target: {project['target']} EGP)")
    
    try:
        choice = int(input("\nSelect project to edit (number): ").strip())
        if 1 <= choice <= len(user_projects):
            project = user_projects[choice - 1]
            
            print("\nLeave field blank to keep current value.")
            new_title = input(f"Title [{project['title']}]: ").strip() or project['title']
            new_details = input(f"Details [{project['details']}]: ").strip() or project['details']
            
            while True:
                new_target = input(f"Target [{project['target']} EGP]: ").strip()
                if not new_target:
                    new_target = project['target']
                    break
                try:
                    new_target = float(new_target)
                    if new_target <= 0:
                        print("Target must be a positive number.")
                        continue
                    break
                except ValueError:
                    print("Invalid amount. Please enter a number.")
            
            # Find the original project in the main projects list
            for p in projects:
                if p['title'] == project['title'] and p['owner_email'] == logged_in_user['email']:
                    p['title'] = new_title
                    p['details'] = new_details
                    p['target'] = new_target
                    break
            
            save_data()
            print("\nProject updated successfully!")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def delete_project():
    user_projects = [p for p in projects if p['owner_email'] == logged_in_user['email']]
    
    if not user_projects:
        print("\nYou don't have any projects to delete.")
        return
    
    print("\n--- Your Projects ---")
    for idx, project in enumerate(user_projects, 1):
        print(f"{idx}. {project['title']} (Target: {project['target']} EGP)")
    
    try:
        choice = int(input("\nSelect project to delete (number): ").strip())
        if 1 <= choice <= len(user_projects):
            project = user_projects[choice - 1]
            
            confirm = input(f"Are you sure you want to delete '{project['title']}'? (y/n): ").strip().lower()
            if confirm == 'y':
                # Remove from main projects list
                projects[:] = [p for p in projects if not (p['title'] == project['title'] and p['owner_email'] == logged_in_user['email'])]
                save_data()
                print("\nProject deleted successfully!")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def search_by_date():
    print("\n--- Search Projects by Date ---")
    print("1. Search by start date")
    print("2. Search by end date")
    print("3. Search by date range")
    
    try:
        choice = int(input("Enter your choice (1-3): ").strip())
        if choice == 1:
            date = input("Enter start date (YYYY-MM-DD): ").strip()
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                filtered = [p for p in projects if datetime.datetime.strptime(p['start_date'], "%Y-%m-%d").date() == date]
                view_projects(lambda x: filtered)
            except ValueError:
                print("Invalid date format.")
        elif choice == 2:
            date = input("Enter end date (YYYY-MM-DD): ").strip()
            try:
                date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
                filtered = [p for p in projects if datetime.datetime.strptime(p['end_date'], "%Y-%m-%d").date() == date]
                view_projects(lambda x: filtered)
            except ValueError:
                print("Invalid date format.")
        elif choice == 3:
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            try:
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
                filtered = [
                    p for p in projects 
                    if start_date <= datetime.datetime.strptime(p['start_date'], "%Y-%m-%d").date() <= end_date
                ]
                view_projects(lambda x: filtered)
            except ValueError:
                print("Invalid date format.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Please enter a valid number.")

def main_menu():
    print("\n--- Main Menu ---")
    if not logged_in_user:
        print("1. Register")
        print("2. Login")
        print("3. View All Projects")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            view_projects()
        elif choice == '4':
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")
    else:
        print("1. Create Project")
        print("2. View All Projects")
        print("3. Edit My Projects")
        print("4. Delete My Projects")
        print("5. Search Projects by Date")
        print("6. Logout")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        if choice == '1':
            create_project()
        elif choice == '2':
            view_projects()
        elif choice == '3':
            edit_project()
        elif choice == '4':
            delete_project()
        elif choice == '5':
            search_by_date()
        elif choice == '6':
            global logged_in_user
            logged_in_user = None
            print("\nLogged out successfully!")
        elif choice == '7':
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")

def main():
    load_data()
    print("Welcome to Crowdfunding Console App!")
    
    while True:
        try:
            main_menu()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            exit()
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()