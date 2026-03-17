import os
import subprocess
import sys

def format_python_file(file_path):
    """Format a Python file using Black."""
    try:
        subprocess.run(['black', file_path], check=True)
        print(f"Formatted: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting {file_path}: {e}")

def check_python_file(file_path):
    """Check a Python file using Flake8."""
    try:
        result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Flake8 issues in {file_path}:\n{result.stdout}")
        else:
            print(f"No Flake8 issues in {file_path}.")
    except FileNotFoundError:
        print(f"Error: flake8 not found. Please install flake8.")
    except Exception as e:
        print(f"Error checking {file_path}: {e}")

def format_and_check_directory(directory):
    """Format and check all Python files in the specified directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                format_python_file(file_path)
                check_python_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python formatter.py <directory>")
        sys.exit(1)

    target_directory = sys.argv[1]

    if not os.path.isdir(target_directory):
        print(f"Error: {target_directory} is not a valid directory.")
        sys.exit(1)

    format_and_check_directory(target_directory)

# TODO: Add support for configuration files to specify file types or exclude certain files.
# TODO: Implement logging instead of print statements for better tracking.
# TODO: Consider adding a dry-run option that shows what would be done without making changes.
