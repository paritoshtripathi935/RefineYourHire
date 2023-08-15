import os

def create_project_structure():
    project_name = "hr_process_optimization"
    directories = [
        "app",
        "app/models",
        "app/routes",
        "app/utils",
    ]
    
    files = [
        "app/__init__.py",
        "app/main.py",
        "app/models/__init__.py",
        "app/models/job.py",
        "app/models/candidate.py",
        "app/models/user.py",
        "app/routes/__init__.py",
        "app/routes/job.py",
        "app/routes/candidate.py",
        "app/routes/auth.py",
        "app/utils/__init__.py",
        "app/utils/nlp.py",
        "app/utils/ranking.py",
        "app/utils/email.py",
        "app/utils/auth.py",
        "requirements.txt",
        ".env",
        ".gitignore",
        "README.md",
        "main.py",
        "database.db",  # SQLite database file
    ]
    
    # Create the project directory
    os.makedirs(project_name, exist_ok=True)
    
    # Create directories
    for directory in directories:
        path = os.path.join(project_name, directory)
        os.makedirs(path, exist_ok=True)
    
    # Create files
    for file in files:
        path = os.path.join(project_name, file)
        with open(path, 'w') as f:
            pass

if __name__ == "__main__":
    create_project_structure()
    print("Project structure created successfully.")
