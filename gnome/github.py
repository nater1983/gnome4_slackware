#!/usr/bin/env python3

import requests
import os

def download_tarball(repo_owner, repo_name, version_or_tag, download_dir="downloads", extract_dir="src"):
    # Prompt user for the subdirectory inside src/
    subdir = input(f"Enter the subdirectory within '{extract_dir}' where you want the tarball saved (e.g., {repo_owner}): ")

    # Check if the version has a "v" prefix, if not add it dynamically
    version_with_v = version_or_tag if version_or_tag.startswith("v") else f"v{version_or_tag}"

    # Construct URLs for both release format with and without "v"
    url_with_v = f"https://github.com/{repo_owner}/{repo_name}/releases/download/{version_with_v}/{repo_name}-{version_with_v[1:]}.tar.xz"
    url_without_v = f"https://github.com/{repo_owner}/{repo_name}/releases/download/{version_or_tag}/{repo_name}-{version_or_tag}.tar.xz"

    # Construct archive URLs for both formats (with and without "v")
    url_archive_with_v = f"https://github.com/{repo_owner}/{repo_name}/archive/{version_with_v}/{repo_name}-{version_with_v[1:]}.tar.gz"
    url_archive_without_v = f"https://github.com/{repo_owner}/{repo_name}/archive/{version_or_tag}/{repo_name}-{version_or_tag}.tar.gz"

    # Try the version with the "v" first, then without it if it fails, and finally check for the archive format
    url = None
    response = requests.get(url_with_v, stream=True)
    if response.status_code == 200:
        url = url_with_v
    else:
        # If the "v" version fails, try the version without it
        response = requests.get(url_without_v, stream=True)
        if response.status_code == 200:
            url = url_without_v
        else:
            # If neither of the above URLs work, try the archive format with "v"
            response = requests.get(url_archive_with_v, stream=True)
            if response.status_code == 200:
                url = url_archive_with_v
            else:
                # Try the archive format without "v"
                response = requests.get(url_archive_without_v, stream=True)
                if response.status_code == 200:
                    url = url_archive_without_v

    # If no valid URL is found, notify the user
    if not url:
        print(f"Failed to find a valid URL for {repo_name} at version {version_or_tag}.")
        print(f"Tried the following URLs:\n - {url_with_v}\n - {url_without_v}\n - {url_archive_with_v}\n - {url_archive_without_v}")
        return

    # Construct the file name and path for the tarball
    tarball_filename = f"{repo_name}-{version_or_tag}.tar.xz" if url == url_without_v or url == url_with_v else f"{repo_name}-{version_or_tag}.tar.gz"
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
    repo_owner = input("Enter the repository owner (e.g., hughsie): ")
    repo_name = input("Enter the repository name (e.g., appstream-glib): ")
    version_or_tag = input("Enter the version or tag (e.g., 1.15.0 or appstream_glib_0_8_3): ")
    
    # Call the function with user input
    download_tarball(repo_owner, repo_name, version_or_tag)
