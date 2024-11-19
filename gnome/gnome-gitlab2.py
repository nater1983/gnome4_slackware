import os
import sys
import urllib.parse
import requests

def fetch_tags(repo_url, access_token=None):
    """
    Fetches all tags from a GitLab repository without cloning it.
    """
    try:
        repo_url = repo_url.strip()  # Remove any leading/trailing spaces

        if not repo_url.startswith("https://gitlab.gnome.org/"):
            raise ValueError("The URL must start with https://gitlab.gnome.org/")

        base_api_url = "https://gitlab.gnome.org/api/v4"
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


def find_latest_version(version, tags):
    """
    Finds the latest version from the tag list, considering both major version changes
    and updates within the current major version.
    """
    # Helper function to parse version strings
    def parse_version(version_str):
        parts = version_str.replace('_', '.').split('.')
        return [int(part) for part in parts] + [0] * (3 - len(parts))  # Ensure three components

    current_major, current_minor, current_patch = parse_version(version)

    # Categorize tags by major version
    version_dict = {}
    for tag in tags:
        try:
            tag_major, tag_minor, tag_patch = parse_version(tag['name'])
            if tag_major not in version_dict:
                version_dict[tag_major] = []
            version_dict[tag_major].append((tag_minor, tag_patch, tag['name']))
        except ValueError:
            # Skip invalid version strings
            continue

    # Find the latest major version
    max_major = max(version_dict.keys())
    if max_major > current_major:
        # New major version found, find the latest version within this major version
        latest_version = max(version_dict[max_major], key=lambda x: (x[0], x[1]))[2]
    else:
        # Within the same major version, find the latest version
        latest_version = None
        for tag_minor, tag_patch, tag_name in version_dict[current_major]:
            if (tag_minor > current_minor or
                (tag_minor == current_minor and tag_patch > current_patch)):
                latest_version = tag_name if not latest_version else max(latest_version, tag_name, key=lambda v: parse_version(v))

    return latest_version


def main():
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
            # Check for a newer version
            newer_version = find_latest_version(project_version, tags)
            if newer_version:
                print(f"Found a newer version: {newer_version}. Downloading the file...")
                download_file(newer_version, project_name)
                update_version_file(project_name, newer_version)  # Update the version file with the new version
            else:
                print(f"No newer version found. Current version: {project_version}.")
        else:
            print(f"Version information not found for project {project_name}. Here are the available tags:")
            for tag in tags:
                print(tag["name"])
    else:
        print("No tags fetched. Please check if the repository URL is correct or if there is an authentication issue.")


if __name__ == "__main__":
    main()
