import os
import sys
import requests
import urllib.parse

# Mapping of project names for repositories that use a different name on GitLab
PROJECT_NAME_MAP = {
    'rest': 'librest',
    # Add any other mappings here
}

def print_debug(message):
    """Print debug messages."""
    print(f"[DEBUG] {message}")

def get_tags_from_gitlab(repo_url, access_token=None):
    """
    Fetches all tags from a GitLab repository without cloning it.
    """
    try:
        repo_url = repo_url.strip()  # Remove any leading/trailing spaces

        if not repo_url.startswith("https://gitlab.gnome.org/"):
            raise ValueError("The URL must start with https://gitlab.gnome.org/")

        base_api_url = "https://gitlab.gnome.org/api/v4"
        project_path = repo_url.replace("https://gitlab.gnome.org/", "").rstrip(".git")

        # Check if the project name has a mapping in the dictionary
        if project_path in PROJECT_NAME_MAP:
            project_path = PROJECT_NAME_MAP[project_path]

        if not project_path:
            raise ValueError("Invalid GitLab repository URL provided.")

        encoded_path = urllib.parse.quote(project_path, safe="")
        tags_url = f"{base_api_url}/projects/{encoded_path}/repository/tags"

        # Debug: print the final URL to verify it's correct
        print_debug(f"Fetching tags from: {tags_url}")

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
            print(f"Error details: {response.text}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching tags: {e}")
        return []
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return []

def parse_version(version_str):
    """
    Parses a version string into a list of integers, filling missing parts with zeros.
    """
    parts = version_str.replace('_', '.').split('.')
    return [int(part) for part in parts] + [0] * (3 - len(parts))  # Ensure three components

def find_newer_version(current_version, tags):
    """
    Finds the newer version from the list of tags, considering both major version changes
    and updates within the current major version.
    """
    # Parse the current version
    current_major, current_minor, current_patch = parse_version(current_version)

    version_dict = {}
    for tag in tags:
        tag_major, tag_minor, tag_patch = parse_version(tag['name'])
        if tag_major not in version_dict:
            version_dict[tag_major] = []
        version_dict[tag_major].append((tag_minor, tag_patch, tag['name']))

    # Debug: print the version dictionary for inspection
    print_debug(f"Version dictionary: {version_dict}")

    # Find the latest major version
    max_major = max(version_dict.keys()) if version_dict else 0
    if max_major > current_major:
        # New major version found, find the latest version within this major version
        latest_version = max(version_dict[max_major], key=lambda x: (x[0], x[1]))[2]
    else:
        # Within the same major version, find the latest version
        latest_version = None
        for tag_minor, tag_patch, tag_name in version_dict[current_major]:
            if (tag_minor > current_minor or
                (tag_minor == current_minor and tag_patch > current_patch)):
                if not latest_version or compare_versions(latest_version, tag_name):
                    latest_version = tag_name

    return latest_version

def compare_versions(version1, version2):
    """
    Compares two version strings and returns True if version1 is newer than version2.
    """
    v1_parts = parse_version(version1)
    v2_parts = parse_version(version2)
    return v1_parts > v2_parts

def process_version_files(version_dir):
    """
    Cycles through all the version files in the specified directory and ensures they are updated.
    """
    # Iterate through all files in the version directory
    for file in os.listdir(version_dir):
        file_path = os.path.join(version_dir, file)
        if os.path.isfile(file_path):
            # Read current version from the version file
            with open(file_path, 'r') as f:
                current_version = f.read().strip()

            # Get the project name from the file (assumed to be the project name in GitLab)
            project_name = file.strip()  # Assuming the file name corresponds to the project name

            print_debug(f"Processing {project_name} with current version {current_version}")

            # Fetch tags from GitLab for this project
            project_url = f"https://gitlab.gnome.org/GNOME/{project_name}"
            tags = get_tags_from_gitlab(project_url)

            if tags:
                # Find the newest version
                newer_version = find_newer_version(current_version, tags)

                # If a newer version is found, update the version file
                if newer_version != current_version:
                    print(f"Updating {file} from {current_version} to {newer_version}")
                    with open(file_path, 'w') as f:
                        f.write(newer_version)
            else:
                print(f"Failed to fetch tags for {project_name}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python gnome-gitlab2.py <version_directory>")
        sys.exit(1)

    version_dir = sys.argv[1]

    if not os.path.isdir(version_dir):
        print(f"Error: {version_dir} is not a valid directory.")
        sys.exit(1)

    print(f"Processing versions in {version_dir}...")
    process_version_files(version_dir)

if __name__ == "__main__":
    main()
