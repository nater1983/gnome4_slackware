#!/usr/bin/env python3

import os
import sys
import urllib.parse
import requests
from datetime import datetime, timedelta
import pytz  # Required for timezone handling

def print_debug(message):
    """
    Helper function to print debug messages.
    """
    print(f"[DEBUG] {message}")

def get_tags_from_gitlab(repo_url, access_token=None):
    """
    Fetches all tags from a GitLab repository without cloning it, filtering out tags older than 9 months,
    but considering tags up to 3 years ago as valid if no tags are within the last 9 months.
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
            tags = response.json()

            # Get the date 9 months ago with timezone awareness (UTC in this case)
            nine_months_ago = datetime.now(pytz.utc) - timedelta(days=9*30)
            three_years_ago = datetime.now(pytz.utc) - timedelta(days=4*365)

            # Filter tags by date, excluding tags older than 9 months, but consider up to 3 years ago as valid
            recent_tags = [
                tag for tag in tags
                if datetime.strptime(tag['commit']['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z") > nine_months_ago
            ]

            # If no tags are within the last 9 months, consider those from the last 3 years
            if not recent_tags:
                recent_tags = [
                    tag for tag in tags
                    if datetime.strptime(tag['commit']['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z") > three_years_ago
                ]
                if recent_tags:
                    print_debug(f"No recent tags found. Using the latest tag from the last 4 years.")
                else:
                    print_debug(f"No valid tags found within the last 4 years.")
            
            return recent_tags
        else:
            print(f"Failed to fetch tags: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching tags: {e}")
        return []
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return []

def parse_version(version_str):
    """
    Parses a version string into a list of integers, handling missing components,
    stripping a leading 'v' if present, and assigning numerical precedence to pre-release labels.
    """
    # Strip the leading 'v' if present (e.g., v47.alpha -> 47.alpha)
    version_str = version_str.lstrip('v')

    # Pre-release labels with numeric precedence (alpha < beta < rc < stable)
    pre_release_map = {
        'alpha': 0,
        'beta': 1,
        'rc': 2,
    }

    # Split the version into parts
    parts = version_str.split('.')

    # Convert version parts into integers, handling pre-release labels
    parsed_parts = []
    for part in parts:
        if part.isdigit():  # Handle numeric components like '47', '0', '1'
            parsed_parts.append(int(part))
        elif part in pre_release_map:  # Handle pre-release labels
            parsed_parts.append(pre_release_map[part])
        else:
            # If part is an invalid string (e.g., a string like 'unstable'), handle it
            parsed_parts.append(0)  # Default value or raise an error if you prefer

    # Ensure three components by padding with zeros if necessary
    return parsed_parts + [0] * (3 - len(parsed_parts))  # Ensure three components

def find_newer_version(current_version, tags):
    """
    Finds the newest version from the tag list compared to the current version.
    """
    current_major, current_minor, current_patch = parse_version(current_version)

    version_dict = {}
    for tag in tags:
        try:
            tag_major, tag_minor, tag_patch = parse_version(tag['name'])
            if tag_major not in version_dict:
                version_dict[tag_major] = []
            version_dict[tag_major].append((tag_minor, tag_patch, tag['name']))
        except ValueError:
            continue

    # Check if version_dict is empty
    if not version_dict:
        print("No valid tags found.")
        return current_version  # Return the current version if no valid tags are found

    max_major = max(version_dict.keys())
    if max_major > current_major:
        return max(version_dict[max_major], key=lambda x: (x[0], x[1]))[2]
    else:
        latest_version = current_version
        for tag_minor, tag_patch, tag_name in version_dict[current_major]:
            if (tag_minor > current_minor or
                (tag_minor == current_minor and tag_patch > current_patch)):
                if not latest_version or tag_name > latest_version:
                    latest_version = tag_name

    return latest_version

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
