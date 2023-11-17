import os
import subprocess


# Function to install or upgrade pip
def install_or_upgrade_pip():
    try:
        subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pip"])
    except Exception as e:
        print(f"Error installing/upgrading pip: {str(e)}")
        exit(1)


# Function to list outdated packages and update them
def list_and_update_packages():
    updated_packages = []
    try:
        # Get the list of outdated packages
        result = subprocess.run(
            [
                "python",
                "-m",
                "pip",
                "list",
                "--outdated",
                "--format=json",
                "--disable-pip-version-check",
            ],
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        outdated_packages_info = result.stdout.strip()

        if outdated_packages_info:
            outdated_packages = [
                package["name"] for package in eval(outdated_packages_info)
            ]
            # Update all outdated packages
            for package in outdated_packages:
                try:
                    # Install the latest version of the package without specifying versions
                    subprocess.run(
                        [
                            "python",
                            "-m",
                            "pip",
                            "install",
                            "--upgrade",
                            "--upgrade-strategy",
                            "only-if-needed",
                            "--disable-pip-version-check",
                            package,
                        ]
                    )
                    updated_packages.append(package)
                except Exception as e:
                    print(f"Error updating {package}: {str(e)}")

    except Exception as e:
        print(f"Error updating packages: {str(e)}")
        exit(1)
    return updated_packages


# Check if pip is installed, if not, install it
try:
    subprocess.run(["python", "-m", "pip", "--version"], stdout=subprocess.DEVNULL)
except FileNotFoundError:
    print("pip is not installed. Installing it...")
    install_or_upgrade_pip()

# List outdated packages and update them
updated_packages = list_and_update_packages()

# Print the names of updated packages
if updated_packages:
    print("Packages updated successfully:")
    for package in updated_packages:
        print(f"- {package}")
else:
    print("No packages were updated.")
