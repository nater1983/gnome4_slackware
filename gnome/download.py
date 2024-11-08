#!/usr/bin/env python3

import requests
import sys
import os

downloads_base_url = "https://download.gnome.org/sources"

def get_pkg_version(project_name):
    version_file_path = os.path.join("version", project_name)
    try:
        with open(version_file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Version file for {project_name} not found at {version_file_path}.")
        return None

def construct_tarball_urls(project_name, pkg_version):
    """Construct URLs for major.minor, major.minor.patch, and major.minor.patch formats."""
    version_parts = pkg_version.split(".")
    urls = []

    if len(version_parts) == 2:  # e.g., 47.1
        major_version = version_parts[0]
        urls.append(f"{downloads_base_url}/{project_name}/{major_version}/{project_name}-{pkg_version}.tar.xz")
    elif len(version_parts) == 3:  # e.g., 47.1.1 or 3.54.1
        if len(version_parts[0]) == 1:  # For cases like 3.54.1
            major_minor_version = f"{version_parts[0]}.{version_parts[1]}"  # Combine major and minor version
            urls.append(f"{downloads_base_url}/{project_name}/{major_minor_version}/{project_name}-{pkg_version}.tar.xz")
        else:
            major_version = version_parts[0]  # For cases like 47.1.1
            urls.append(f"{downloads_base_url}/{project_name}/{major_version}/{project_name}-{pkg_version}.tar.xz")
    else:
        print(f"Invalid version format for {pkg_version}")
    
    return urls

def check_tarball_availability(tarball_url):
    try:
        response = requests.head(tarball_url)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Failed to connect to {tarball_url}. Error: {e}")
        return False

def download_tarball(tarball_url, target_directory):
    tarball_name = os.path.basename(tarball_url)
    tarball_path = os.path.join(target_directory, tarball_name)
    if os.path.exists(tarball_path):
        print(f"{tarball_name} already exists in {target_directory}. Skipping download.")
        return
    try:
        with requests.get(tarball_url, stream=True) as response:
            response.raise_for_status()
            with open(tarball_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        print(f"Downloaded {tarball_name} to {target_directory}")
    except requests.RequestException as e:
        print(f"Failed to download {tarball_name} from {tarball_url}. Error: {e}")

if len(sys.argv) < 2:
    print("Usage: python gnome.py <directory>:<project_name>")
    sys.exit(1)

arg = sys.argv[1]
if ':' not in arg:
    print("Invalid format. Use <directory>:<project_name>.")
    sys.exit(1)

directory, project_name = arg.split(':', 1)
src_directory = os.path.join("src", directory)
os.makedirs(src_directory, exist_ok=True)

pkg_version = get_pkg_version(project_name)
if not pkg_version:
    sys.exit(1)

# Construct URLs and attempt download for both formats
urls = construct_tarball_urls(project_name, pkg_version)
downloaded = False

for url in urls:
    if check_tarball_availability(url):
        print(f"{project_name} download link found: {url}")
        download_tarball(url, src_directory)
        downloaded = True
        break

if not downloaded:
    print(f"Tarball for {project_name} version {pkg_version} not found on GNOME's downloads server.")
