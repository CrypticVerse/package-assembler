import subprocess
from PackageAssembler.Functions import PackageInfoCollector

def get_input(prompt, help):
    """Ask for user input."""
    while True:
        user = input(prompt)
        if user in ['?', 'help', ' ']:
            print(help)
        elif user in ['exit', 'quit', 'abort']:
            print("Exiting...")
            sys.exit()
        else:
            return user

def new_version():
    package_name = subprocess.run(f"cat debian/control | grep Source | awk '{{print $2}}'", shell=True, check=True, stdout=subprocess.PIPE, text=True)
    new_package_version = get_input("Please enter the new version (? for extra cmds): ", "Cmds:\n <version_number> for different number\n +d to add debian revision\n +v to bump version")
    try:
        subprocess.run(f"echo {new_package_version} lol {package_name.stdout.strip()} is the name", shell=True, check=True)
    except Exception as e:
        print(f"Exception is {e}")
