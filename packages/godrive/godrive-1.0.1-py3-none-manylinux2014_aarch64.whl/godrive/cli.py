import os
import platform
import subprocess
import sys

def main():
    # Detect OS and architecture
    system = platform.system().lower()
    arch = platform.machine().lower()

    # Determine the correct binary
    binary_name = "godrive"
    if system == "windows":
        binary_name = "godrive.exe"
    elif system == "linux" and arch == "x86_64":
        binary_name = "godrive-linux-amd64"
    elif system == "linux" and arch in ("aarch64", "arm64"):
        binary_name = "godrive-linux-arm64"
    elif system == "darwin" and arch == "x86_64":
        binary_name = "godrive-macos-amd64"
    elif system == "darwin" and arch == "arm64":
        binary_name = "godrive-macos-arm64"
    else:
        print(f"Unsupported OS/Arch: {system} {arch}")
        sys.exit(1)

    # Get the path of this script
    package_dir = os.path.dirname(os.path.abspath(__file__))

    # Paths to executables
    go_binary = os.path.join(package_dir, binary_name)
    upload_script = os.path.join(package_dir, "godrive_upload")

    # Ensure both files exist
    if not os.path.exists(go_binary) or not os.path.exists(upload_script):
        print("Error: Required executable files not found!")
        sys.exit(1)

    # Make sure they are executable
    os.chmod(go_binary, 0o755)
    os.chmod(upload_script, 0o755)

    # Run the Go binary (which internally calls godrive_upload)
    subprocess.run([go_binary] + sys.argv[1:])

if __name__ == "__main__":
    main()
