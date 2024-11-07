#!/usr/bin/env python3

import requests
import sys
import os

# Base URL and GNOME version
downloads_base_url = "https://download.gnome.org/sources"

# Function to read the package version from the specified version file
def get_pkg_version(project_name):
    version_file_path = os.path.join("version", project_name)
    try:
        with open(version_file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Version file for {project_name} not found at {version_file_path}.")
        return None

# Function to check if tarball is available on GNOME's downloads server using GET request
def check_tarball_availability(project_name, pkg_version):
    # Handle .0 removal for the directory path but keep it for the filename
    if pkg_version.endswith(".0"):
        major_version = pkg_version[:-2]  # Remove the last two characters ".0"
        tarball_url = f"{downloads_base_url}/{project_name}/{major_version}/{project_name}-{pkg_version}.tar.xz"  # Use original version for filename
    else:
        major_version = pkg_version  # No change if there's no ".0"
        tarball_url = f"{downloads_base_url}/{project_name}/{major_version[:2]}/{project_name}-{pkg_version}.tar.xz"  # Use version for filename

    print(f"Checking URL: {tarball_url}")  # Debugging line to print the URL
    
    response = requests.get(tarball_url)  # Use GET to check if the file exists and retrieve the response
    print(f"Response Status Code: {response.status_code}")  # Print the response status code

    if response.status_code == 200:
        return tarball_url
    else:
        print(f"Error: {response.status_code} - {response.text}")  # Print any errors returned by the server
        return None

# Function to download the tarball
def download_tarball(tarball_url, target_directory):
    tarball_name = tarball_url.split("/")[-1]
    tarball_path = os.path.join(target_directory, tarball_name)
    response = requests.get(tarball_url, stream=True)
    if response.status_code == 200:
        with open(tarball_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {tarball_name} to {target_directory}\n")
    else:
        print(f"Failed to download {tarball_name} from {tarball_url}")

# Main execution
if len(sys.argv) < 2:
    print("Please provide a directory and project name in the format <directory>:<project_name>. Usage: python gnome.py <directory>:<project_name>")
    sys.exit(1)

# Parse the directory and project name from the command-line argument
arg = sys.argv[1]
if ':' not in arg:
    print("Invalid format. Use <directory>:<project_name>.")
    sys.exit(1)

directory, project_name = arg.split(':', 1)

# Ensure the src directory exists for the specified project
src_directory = os.path.join("src", directory)
os.makedirs(src_directory, exist_ok=True)

# Get the package version
pkg_version = get_pkg_version(project_name)

if not pkg_version:
    print("Package version not specified or version file not found, exiting.")
    sys.exit(1)

# Check for the tarball on the GNOME downloads server
tarball_url = check_tarball_availability(project_name, pkg_version)

if tarball_url:
    print(f"{project_name} download link: {tarball_url}\n")
    download_tarball(tarball_url, src_directory)
else:
    print(f"Tarball for {project_name} version {pkg_version} not found on GNOME's downloads server.\n")
