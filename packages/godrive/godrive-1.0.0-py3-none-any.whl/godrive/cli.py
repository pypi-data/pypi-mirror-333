import os
import sys
import subprocess

HELP_TEXT = """
Don't know how to use :
Go to https://github.com/rohanbhatotiya/godrive
"""

def main():
    # Determine the installation directory
    package_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the godrive executable
    godrive_exec = os.path.join(package_dir, "godrive")

    # Ensure the executable exists
    if not os.path.isfile(godrive_exec):
        print("❌ Error: godrive executable not found. Please reinstall Godrive.")
        sys.exit(1)

    # Handle `--help` manually
    if len(sys.argv) > 1 and sys.argv[1] in ["--help", "help"]:
        print(HELP_TEXT)
        sys.exit(0)

    # Make sure it is executable
    os.chmod(godrive_exec, 0o755)

    # Run the executable with user-provided arguments
    try:
        subprocess.run([godrive_exec] + sys.argv[1:], check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)

if __name__ == "__main__":
    main()
