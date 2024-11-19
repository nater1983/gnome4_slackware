import requests
import urllib.parse
import sys
import os

def fetch_tags(repo_url, access_token=None):
    """
    Fetches all tags from a GitLab repository without cloning it.
    """
    try:
        repo_url = repo_url.strip()  # Remove any leading/trailing spaces
        
        if not repo_url.startswith("https://gitlab.gnome.org/"):
            raise ValueError("The URL must start with https://gitlab.gnome.org/")
        
      # Check if it's under 'GNOME' or 'World' namespace
        if "GNOME" in repo_url:
            base_api_url = "https://gitlab.gnome.org/api/v4"
        elif "World" in repo_url:
            base_api_url = "https://gitlab.gnome.org/api/v4"
        else:
            raise ValueError("Unsupported GitLab namespace. Only GNOME and World are supported.")
            
        project_path = repo_url.replace("https://gitlab.gnome.org/", "").rstrip(".git")
        
        if not project_path:
            raise ValueError("Invalid GitLab repository URL provided.")
        
        encoded_path = urllib.parse.quote(project_path, safe="")
        tags_url = f"{base_api_url}/projects/{encoded_path}/repository/tags"
        
        headers = {}
        if access_token:
            headers["Private-Token"] = access_token

        # Send the GET request to fetch the tags
        response = requests.get(tags_url, headers=headers)

        # Debugging: print the raw response to help with troubleshooting
        print(f"Response status code: {response.status_code}")
        #print(f"Response content: {response.text}")  # This will show the raw content

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Returns a list of tag info
        else:
            print(f"Failed to fetch tags: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching tags: {e}")
        return []
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return []

def get_version_from_file(project_name):
    """
    Retrieves the version from the version file for the project.
    """
    version_file_path = f"version/{project_name}"
    
    if os.path.exists(version_file_path):
        try:
            with open(version_file_path, "r") as file:
                version = file.read().strip()
                return version
        except Exception as e:
            print(f"An error occurred while reading version file: {e}")
            return None
    else:
        print(f"Version file for {project_name} not found.")
        return None

def download_file(tag, project_name):
    """
    Downloads the file for the specified tag from the GitLab repository and saves it in the 'src/' directory.
    """
    os.makedirs("src", exist_ok=True)

    download_url = f"https://gitlab.gnome.org/GNOME/{project_name}/-/archive/{tag}/{project_name}-{tag}.tar.gz"
    print(f"Downloading file from: {download_url}")
    response = requests.get(download_url)

    if response.status_code == 200:
        file_name = f"src/{project_name}-{tag}.tar.gz"
        with open(file_name, "wb") as file:
            file.write(response.content)
        print(f"File downloaded to: {file_name}")
    else:
        print(f"Failed to download the file for tag {tag}")

def print_tags_and_download_url(tags, project_name):
    """
    Prints the tag list and their download URLs.
    """
    if not tags:
        print("No tags found.")
        return

    for tag in tags:
        download_url = f"https://gitlab.gnome.org/GNOME/{project_name}/-/archive/{tag['name']}/{project_name}-{tag['name']}.tar.gz"
        print(f"Tag: {tag['name']}")
        print(f"Download URL: {download_url}\n")

def compare_versions(version1, version2):
    """
    Compares two version strings and returns True if version1 is older than version2.
    """
    # Normalize version strings by replacing underscores with dots
    version1 = version1.replace('_', '.')
    version2 = version2.replace('_', '.')

    # Split version strings into lists of integers
    version1_parts = [int(part) for part in version1.split('.')]
    version2_parts = [int(part) for part in version2.split('.')]

    # Pad the shorter version with zeros to make both lists the same length
    length = max(len(version1_parts), len(version2_parts))
    version1_parts.extend([0] * (length - len(version1_parts)))
    version2_parts.extend([0] * (length - len(version2_parts)))

    # Compare part by part
    for v1, v2 in zip(version1_parts, version2_parts):
        if v1 < v2:
            return True  # version1 is older
        elif v1 > v2:
            return False  # version2 is older

    return False  # versions are equal

def find_newer_version(version, tags):
    """
    Finds the newest version from the tag list that is newer than the given version.
    """
    newer_version = None
    for tag in tags:
        if compare_versions(version, tag['name']):
            if newer_version is None or compare_versions(newer_version, tag['name']):
                newer_version = tag['name']
    return newer_version

def update_version_file(project_name, new_version):
    """
    Updates the version file for the project with the new version.
    """
    version_file_path = f"version/{project_name}"
    try:
        with open(version_file_path, "w") as file:
            file.write(new_version)
        print(f"Updated version file: {version_file_path} to version {new_version}")
    except Exception as e:
        print(f"An error occurred while updating the version file: {e}")

# Example: Input URL from command line argument
if len(sys.argv) < 2:
    print("Usage: python t.py <GitLab repository URL>")
    sys.exit(1)

repo_url = sys.argv[1]

# Optional: Add your personal access token if the repository is private
access_token = None  # Replace with your token if needed

# Extract the project name from the repository URL
project_name = repo_url.split("/")[-1]  # Assuming project name is the last part of the URL

# Fetch tags from GitLab
tags = fetch_tags(repo_url, access_token)

if tags:  # If tags were fetched successfully
    # Get the version from the version/$projectname file
    project_version = get_version_from_file(project_name)

    if project_version:
        # Check if the project version matches any of the tags
        matching_tag = None
        for tag in tags:
            if tag['name'] == project_version:
                matching_tag = tag['name']
                break

        if matching_tag:
            print(f"Version {project_version} matches a tag! Downloading the file...")
            download_file(matching_tag, project_name)
        else:
            # Look for a newer version
            newer_version = find_newer_version(project_version, tags)
            if newer_version:
                print(f"Found a newer version: {newer_version}. Downloading the file...")
                download_file(newer_version, project_name)
                update_version_file(project_name, newer_version)  # Update the version file with the new version
            else:
                print(f"Version {project_version} does not match any tag. Here are the available tags:")
                print_tags_and_download_url(tags, project_name)
    else:
        # No version information found, print the tag list
        print(f"Version information not found for project {project_name}. Here are the available tags:")
        print_tags_and_download_url(tags, project_name)
else:
    print("No tags fetched. Please check if the repository URL is correct or if there is an authentication issue.")

