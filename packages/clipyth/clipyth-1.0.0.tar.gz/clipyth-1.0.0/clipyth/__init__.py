import os 
import sys
import argparse
import shutil
from pathlib import Path

def create_console_app(project_name):
    """
    Creates a new console application with the given name
    """
    # Get current working directory
    cwd = os.getcwd()

    # Create project directory
    project_dir = os.path.join(cwd, project_name)
    os.makedirs(project_dir, exist_ok=True)

    # Create main.py file
    with open(os.path.join(project_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write('''def main():
    print("Hello from your new console application!)

                
if __name__ == "__main__":
    main()
''')
    
    # Create requirements.txt file
    with open(os.path.join(project_dir, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write('# Add your dependencies here\n')
    
    # Create a basic README.md
    with open(os.path.join(project_dir, "README.md"), "w", enconding="utf-8") as f:
        f.write(f'''# {project_name}

A Python console application.

## Getting Started

1. Install dependencies: `pip install -r requirements.txt`
2. Run the application: `python main.py`
''')
        
    print(f"✓ Console application '{project_name}' created successfully!")

def main():
    parser = argparse.ArgumentParser(description="ProjCreator - Python Project Generator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Create the 'new' command
    new_parser = subparsers.add_parser("new", help="Create a new project")
    new_parser.add_argument("template", choices=["console"], help="Project template")
    new_parser.add_argument("project_name", nargs="?", default="my-project", help="Name of the project")

    # Parse arguments
    args = parser.parse_args()

    if args.command == "new":
        if args.template == "console":
            create_console_app(args.project_name)
        else:
            print(f"Unknown template: {args.template}")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()