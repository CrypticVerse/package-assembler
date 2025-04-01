"""Misc functions and questions during the package creation/modification process"""
import subprocess
import sys

class PackageInfoCollector:
    """Collect all necessary information to create a Debian package."""
    def __init__(self):
        # Initialize with default values
        self.valid_archs = subprocess.run(
            ["dpkg-architecture", "-L"], check=True, stdout=subprocess.PIPE
        ).stdout.decode().split("\n")
        self.package_name = None
        self.package_version = None
        self.user_email = None
        self.user_name = None
        self.build_depends = None
        self.arch = None
        self.deps = None
        self.install_files = None
        self.is_native = None
        self.debian_directory = "debian"

    def get_input(self, prompt, help_message):
        """Ask for user input."""
        while True:
            user = input(prompt)
            if user in ['?', 'help', ' ']:
                print(help_message)
            elif user in ['exit', 'quit', 'abort']:
                print("Exiting...")
                sys.exit()
            else:
                return user

    def get_architecture(self, prompt, help_message):
        """Get the architecture of the package."""
        while True:
            arch = self.get_input(prompt, help_message)
            if arch in self.valid_archs or arch == 'any':
                return arch
            else:
                print("Invalid architecture. Please try again.")

    def is_native_package(self, prompt, help_message):
        """Ask if the package is native or non-native."""
        while True:
            is_native_pkg = self.get_input(prompt, help_message)
            if is_native_pkg in ['yes', 'y', 'true']:
                self.is_native = True
                return is_native_pkg
            elif is_native_pkg in ['no', 'n', 'false']:
                self.is_native = False
                return is_native_pkg
            else:
                print("Invalid answer. Valid answers are yes/no, y/n, and true/false")

    def collect_info(self):
        """Collect all necessary information."""
        self.package_name = self.get_input("Please enter the name of your package: ", "Description: Enter the name of your package (e.g., 'mypackage').")
        self.package_version = self.get_input("Please enter the version of your package: ", "Description: Enter the version of your package (e.g., '1.0.0').")
        self.user_email = self.get_input("Please enter your email address: ", "Description: Enter your email address.")
        self.user_name = self.get_input("Please enter your name: ", "Description: Enter your name.")
        self.arch = self.get_architecture("Please enter the architecture of your package. Type any for any arch: ", f"{', '.join(self.valid_archs)}")
        self.is_native_package("Please enter if your package is a native or non-native package: ", "Yes means this package is ONLY for debian.\n No means that this package has an upstream source, and you are repackaging it for Debian")
        self.build_depends = self.get_input("Please enter the apt packages used to build your package separated by commas: ", "Description: Enter the build dependencies for your package (e.g., 'python3-all' for python or 'cpp-14' for c++).")
        self.deps = self.get_input("Please enter the apt packages used to run your package separated by commas: ", "Description: Enter the dependencies for your package (e.g., 'python3' for python or 'cpp-14' for c++).")
        install_files_input = self.get_input("Please enter the files to install separated by commas (please type help, they explain it better): ",
                 "Description: IMPORTANT! ALL INSTALLED FILES ARE FROM THE ROOT PROJECT DIR, NOT THE debian/ DIR!\n entering file1, /usr, file2 /bin will install file1 to /usr and file2 to /bin")

        install_files_list = install_files_input.split(",")
        self.install_files = []

        if len(install_files_list) % 2 != 0:
            print("Error: The number of files and paths must be equal.")
            sys.exit(1)
        for i in range(0, len(install_files_list), 2):
            file = install_files_list[i].strip()
            path = install_files_list[i + 1].strip()
            self.install_files.append((file, path))

    def get_debian_directory(self):
        """Return the debian directory."""
        return self.debian_directory
