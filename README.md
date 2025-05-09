# Crowd-Funding Console App (Python)

A simple command-line application that simulates a crowdfunding platform, where users can create fundraising projects and interact with them through registration, login, and project management features.

##  Features

### Authentication System
- **User Registration**  
  Collects:
  - First Name
  - Last Name
  - Email (validated)
  - Password + Confirm Password
  - Egyptian Mobile Phone Number (validated)

- **Login**  
  Allows a registered user to login using email and password.

### Project Management
Once logged in, the user can:

- **Create a Project**  
  Each project includes:
  - Title
  - Details
  - Target Amount (e.g., 250000 EGP)
  - Start Date & End Date (with validation)

- **View Projects**  
  Display all created projects.

- **Edit Project**  
  Users can edit only their own projects.

- **Delete Project**  
  Users can delete only their own projects.

- **Search by Date** (Bonus)

##  Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/Aya123O/Crowd-Funding-Console-App-Python.git
   cd Crowd-Funding-Console-App-Python
