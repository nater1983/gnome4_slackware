#!/usr/bin/env python3

import requests
import os

def download_tarball_from_gitlab(domain, namespace, repo_name, version, extract_dir="src"):
    # Prompt user for the subdirectory inside src/
    subdir = input(f"Enter the subdirectory within '{extract_dir}' where you want the tarball saved (e.g., {repo_name}): ")

    # Check if the domain is gitlab.com or gitlab.freedesktop.org and build the URL accordingly
    if domain == "gitlab.freedesktop.org":
        url = f"https://{domain}/{namespace}/{repo_name}/-/releases/{version}/downloads/{repo_name}-{version}.tar.xz"
    else:
        url = f"https://{domain}/{namespace}/{repo_name}/-/releases/{version}/downloads/{repo_name}-{version}.tar.xz"

    # Construct the filename and path where the tarball will be saved
    tarball_filename = f"{repo_name}-{version}.tar.xz"
    tarball_path = os.path.join(extract_dir, subdir, tarball_filename)

    # Check if the tarball already exists in the specified subdirectory
    if os.path.exists(tarball_path):
        print(f"{tarball_filename} already exists in {os.path.join(extract_dir, subdir)}. Skipping download.")
    else:
        print(f"Checking tarball URL: {url}")
        # Make a GET request to fetch the tarball
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            # Ensure the specified subdirectory exists
            os.makedirs(os.path.join(extract_dir, subdir), exist_ok=True)

            # Download the tarball if it does not exist
            with open(tarball_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Tarball downloaded successfully: {tarball_path}")
        else:
            print(f"Failed to download tarball. HTTP Status Code: {response.status_code}")


if __name__ == "__main__":
    # Get dynamic input for project details
    domain = input("Enter the GitLab domain (e.g., gitlab.com or gitlab.freedesktop.org): ")
    namespace = input("Enter the GitLab namespace (e.g., emersion): ")
    repo_name = input("Enter the repository name (e.g., libdisplay-info): ")
    version = input("Enter the version (e.g., 0.2.0): ")

    # Call the function with user input
    download_tarball_from_gitlab(domain, namespace, repo_name, version)
