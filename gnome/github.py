#!/usr/bin/env python3

import requests
import os

def download_tarball(repo_owner, repo_name, version_or_tag, download_dir="downloads", extract_dir="src"):
    subdir = input(f"Enter the subdirectory within '{extract_dir}' where you want the tarball saved (e.g., {repo_owner}): ")

    version_with_v = version_or_tag if version_or_tag.startswith("v") else f"v{version_or_tag}"

    # Construct URLs
    url_with_v = f"https://github.com/{repo_owner}/{repo_name}/releases/download/{version_with_v}/{repo_name}-{version_with_v[1:]}.tar.xz"
    url_without_v = f"https://github.com/{repo_owner}/{repo_name}/releases/download/{version_or_tag}/{repo_name}-{version_or_tag}.tar.xz"
    url_archive_with_v = f"https://github.com/{repo_owner}/{repo_name}/archive/{version_with_v}.tar.gz"
    url_archive_without_v = f"https://github.com/{repo_owner}/{repo_name}/archive/{version_or_tag}.tar.gz"
    url_archive_w_v = f"https://github.com/{repo_owner}/{repo_name}/releases/download/{repo_name}-{version_or_tag}/{repo_name}-{version_or_tag}.tar.gz"

    # Attempt to find a valid URL in order of preference
    url = None

    # Check URL with "v" prefix
    print(f"Checking URL: {url_with_v}")
    response = requests.get(url_with_v, stream=True)
    if response.status_code == 200:
        url = url_with_v
    else:
        # Check URL without "v" prefix
        print(f"Checking URL: {url_without_v}")
        response = requests.get(url_without_v, stream=True)
        if response.status_code == 200:
            url = url_without_v
        else:
            # Check archive URL with "v" prefix
            print(f"Checking URL: {url_archive_with_v}")
            response = requests.get(url_archive_with_v, stream=True)
            if response.status_code == 200:
                url = url_archive_with_v
            else:
                # Check archive URL without "v" prefix
                print(f"Checking URL: {url_archive_without_v}")
                response = requests.get(url_archive_without_v, stream=True)
                if response.status_code == 200:
                    url = url_archive_without_v
                else:
                    # Check the additional archive URL format
                    print(f"Checking URL: {url_archive_w_v}")
                    response = requests.get(url_archive_w_v, stream=True)
                    if response.status_code == 200:
                        url = url_archive_w_v

    if not url:
        print(f"Failed to find a valid URL for {repo_name} at version {version_or_tag}.")
        print(f"Tried the following URLs:\n - {url_with_v}\n - {url_without_v}\n - {url_archive_with_v}\n - {url_archive_without_v}\n - {url_archive_w_v}")
        return

    tarball_filename = f"{repo_name}-{version_or_tag}.tar.xz" if url in [url_with_v, url_without_v] else f"{repo_name}-{version_or_tag}.tar.gz"
    tarball_path = os.path.join(extract_dir, subdir, tarball_filename)

    if os.path.exists(tarball_path):
        print(f"{tarball_filename} already exists in {os.path.join(extract_dir, subdir)}. Skipping download.")
    else:
        print(f"Downloading tarball from URL: {url}")

        # Make a GET request to fetch the tarball
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(os.path.join(extract_dir, subdir), exist_ok=True)

            with open(tarball_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Tarball downloaded successfully: {tarball_path}")
        else:
            print(f"Failed to download tarball. HTTP Status Code: {response.status_code}")


if __name__ == "__main__":
    repo_owner = input("Enter the repository owner (e.g., hughsie): ")
    repo_name = input("Enter the repository name (e.g., appstream-glib): ")
    version_or_tag = input("Enter the version or tag (e.g., 1.15.0 or appstream_glib_0_8_3): ")

    download_tarball(repo_owner, repo_name, version_or_tag)
