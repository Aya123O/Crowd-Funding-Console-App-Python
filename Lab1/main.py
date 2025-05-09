from auth import register, login, logout
from project import create_project, view_projects, edit_project, delete_project, search_by_date

def main():
    current_user = None

    while True:
        if not current_user:
            print("\n1 - Register\n2 - Login\n0 - Exit")
            choice = input("Choose: ")
            if choice == "1":
                register()
            elif choice == "2":
                current_user = login()
            elif choice == "0":
                break
            else:
                print("Invalid choice.")
        else:
            print(f"\nLogged in as: {current_user['email']}")
            print("1 - Create Project\n2 - View Projects\n3 - Edit Project\n4 - Delete Project\n5 - Search by Date\n6 - Logout")
            choice = input("Choose: ")
            if choice == "1":
                create_project(current_user)
            elif choice == "2":
                view_projects()
            elif choice == "3":
                edit_project(current_user)
            elif choice == "4":
                delete_project(current_user)
            elif choice == "5":
                search_by_date()
            elif choice == "6":
                logout()
                current_user = None
            else:
                print("Invalid option.")

if __name__ == "__main__":
    main()
    print("Goodbye!")
