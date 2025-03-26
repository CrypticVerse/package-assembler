"""Module to create a new debian package"""
import glob
import os
import subprocess
import sys
from PackageAssembler.Functions import PackageInfoCollector

def create():
    """Creates a new package"""
    collector = PackageInfoCollector()

    collector.collect_info()

    package_name = collector.package_name
    package_version = collector.package_version
    user_email = collector.user_email
    user_name = collector.user_name
    build_depends = collector.build_depends
    arch = collector.arch
    deps = collector.deps
    is_native = collector.is_native
    install_files = collector.install_files
    debian_directory = collector.get_debian_directory()

    subprocess.run(f"mkdir -p {debian_directory}/source && touch {debian_directory}/changelog", shell=True, check=True)
    print(is_native)
    if is_native is False:
        print("Finding upstream source...")
        source = os.path.join("..", "*.orig.tar.*")
        pattern = glob.glob(source)
        if pattern:
            print("Found source!")
        else:
            no_source = input("No source found! Are you sure you want to continue? (y/n): ")
            if no_source.lower() == "n":
                print("Exiting the script as per user input...")
                sys.exit(0)
            elif no_source.lower() == "y":
                print("Continuing despite no source being found...")
            else:
                print("Invalid input. Exiting.")
                sys.exit(1)

    with open(f"{debian_directory}/control", encoding="utf-8") as f:
        print("Writing control file...")
        f.write(f"Source: {package_name}\n")
        f.write("Priority: optional\n")
        f.write(f"Maintainer: {user_name} <{user_email}>\n")
        f.write(f"Build-Depends: debhelper-compat (= 13), {build_depends}\n")
        f.write("Standards-Version: 4.7.2\n\n")
        f.write(f"Package: {package_name}\n")
        f.write(f"Architecture: {arch}\n")
        f.write(f"Depends: {deps}\n")
    with open(f"{debian_directory}/install", encoding="utf-8") as f:
        for file, path in install_files:
            f.write(f"{file} {path}\n")

    with open(f"{debian_directory}/rules", encoding="utf-8") as f:
        print("Writing rules file...")
        f.write("#!/usr/bin/make -f\n\n")
        f.write("%:\n")
        f.write("\tdh $@\n")
    with open(f"{debian_directory}/source/format", encoding="utf-8") as f:
        print("Writing source...")
        if is_native is True:
            f.write("3.0 (native)\n")
        elif is_native is False:
            f.write("3.0 (quilt)\n")
        else:
            sys.exit(1)

    subprocess.run(f"export DEBEMAIL={user_email}", shell=True, check=True)
    subprocess.run(f"export DEBFULLNAME={user_name}", shell=True, check=True)

    try:
        subprocess.run(f"dch -v {package_version} --package {package_name} -D unstable", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)
