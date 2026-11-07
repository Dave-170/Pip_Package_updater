import json
import subprocess
import sys

# Run pip through the interpreter running this script, so the packages that
# get updated are the ones this Python (or venv) actually uses.
PIP = [sys.executable, "-m", "pip", "--disable-pip-version-check"]


# Function to make sure pip is available, bootstrapping it if it isn't
def ensure_pip():
    check = subprocess.run(PIP + ["--version"], capture_output=True)
    if check.returncode == 0:
        return
    print("pip is not installed. Installing it...")
    result = subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"])
    if result.returncode != 0:
        print("Could not install pip. Install it manually and try again.")
        sys.exit(1)


# Function to list outdated packages
def get_outdated_packages():
    result = subprocess.run(
        PIP + ["list", "--outdated", "--format=json"],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    return [package["name"] for package in json.loads(result.stdout or "[]")]


# Function to update outdated packages, returning (updated, failed)
def update_packages(packages):
    updated_packages = []
    failed_packages = []
    for package in packages:
        result = subprocess.run(
            PIP
            + [
                "install",
                "--upgrade",
                "--upgrade-strategy",
                "only-if-needed",
                package,
            ]
        )
        if result.returncode == 0:
            updated_packages.append(package)
        else:
            failed_packages.append(package)
    return updated_packages, failed_packages


def main():
    ensure_pip()

    try:
        outdated_packages = get_outdated_packages()
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Error listing outdated packages: {e}")
        sys.exit(1)

    updated_packages, failed_packages = update_packages(outdated_packages)

    # Print the names of updated packages
    if updated_packages:
        print("Packages updated successfully:")
        for package in updated_packages:
            print(f"- {package}")
    else:
        print("No packages were updated.")

    if failed_packages:
        print("Packages that failed to update:")
        for package in failed_packages:
            print(f"- {package}")
        sys.exit(1)


if __name__ == "__main__":
    main()
