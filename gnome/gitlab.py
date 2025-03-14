#!/usr/bin/env python3

import requests
import os

def download_tarball_from_gitlab(domain, namespace, repo_name, version, extract_dir="src"):
    # Prompt user for the subdirectory inside src/
    subdir = input(f"Enter the subdirectory within '{extract_dir}' where you want the tarball saved (e.g., {repo_name}): ")

    # Clean up the version string by removing unwanted backslashes and ensuring proper "v" prefix formatting
    version_cleaned = version.replace("\\", "")  # Remove any escape characters

    # Generate both possible URLs: with/without "v" prefix and .tar.xz or .tar.gz formats
    urls = [
        f"https://{domain}/{namespace}/{repo_name}/-/releases/{version_cleaned}/downloads/{repo_name}-{version_cleaned}.tar.xz",
        f"https://{domain}/{namespace}/{repo_name}/-/releases/v{version_cleaned}/downloads/{repo_name}-v{version_cleaned}.tar.xz",
        f"https://{domain}/{namespace}/{repo_name}/-/releases/{version_cleaned}/archive/{repo_name}-{version_cleaned}.tar.xz",
        f"https://{domain}/{namespace}/{repo_name}/-/releases/v{version_cleaned}/archive/{repo_name}-v{version_cleaned}.tar.xz",
        f"https://{domain}/{namespace}/{repo_name}/-/releases/{version_cleaned}/downloads/{repo_name}-{version_cleaned}.tar.gz",
        f"https://{domain}/{namespace}/{repo_name}/-/releases/v{version_cleaned}/downloads/{repo_name}-v{version_cleaned}.tar.gz",
        f"https://{domain}/{namespace}/{repo_name}/-/archive/{version_cleaned}/{repo_name}-{version_cleaned}.tar.gz",
        f"https://{domain}/{namespace}/{repo_name}/-/archive/v{version_cleaned}/{repo_name}-v{version_cleaned}.tar.gz"
    ]

    # Determine the tarball filename based on the URLs being checked
    tarball_filename = f"{repo_name}-{version_cleaned}.tar.xz" if "tar.xz" in urls[0] else f"{repo_name}-{version_cleaned}.tar.gz"
    tarball_path = os.path.join(extract_dir, subdir, tarball_filename)

    # Check if the tarball already exists in the specified subdirectory
    if os.path.exists(tarball_path):
        print(f"{tarball_filename} already exists in {os.path.join(extract_dir, subdir)}. Skipping download.")
        return

    # Attempt to download the tarball, trying each URL in order
    for url in urls:
        print(f"Checking tarball URL: {url}")
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            # Ensure the specified subdirectory exists
            os.makedirs(os.path.join(extract_dir, subdir), exist_ok=True)

            # Download the tarball
            with open(tarball_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Tarball downloaded successfully: {tarball_path}")
            return  # Exit the function after a successful download
        elif response.status_code != 404:
            print(f"Failed to download tarball. HTTP Status Code: {response.status_code}")

    # If none of the URLs worked and no 200 status was received, print not found
    print(f"Tarball for {repo_name} version {version_cleaned} not found on GitLab.")

if __name__ == "__main__":
    # Get dynamic input for project details
    domain = input("Enter the GitLab domain (e.g., gitlab.com or gitlab.freedesktop.org): ")
    namespace = input("Enter the GitLab namespace (e.g., emersion): ")
    repo_name = input("Enter the repository name (e.g., libdisplay-info): ")
    version = input("Enter the version (e.g., 0.2.0 or v1.5.0): ")

    # Call the function with user input
    download_tarball_from_gitlab(domain, namespace, repo_name, version)
