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
    Parses a version string into a list of integers, handling missing components
    and assigning a lower precedence to pre-release versions like alpha, beta, rc.
    """
    # Strip the leading 'v' if present (e.g., v3.4.9 -> 3.4.9)
    version_str = version_str.lstrip('v')
    
    # Handle special suffixes
    suffix_map = {
        'alpha': 0,
        'beta': 1,
        'rc': 2,
        'dev': -1,  # Lower precedence than alpha, beta, and rc
    }
    
    parts = version_str.replace('_', '.').split('.')
    
    # Convert suffixes to numeric values for comparison
    for idx, part in enumerate(parts):
        if part in suffix_map:
            parts[idx] = str(suffix_map[part])
    
    # Replace non-numeric parts with '0' for comparison
    parts = [int(part) if part.isdigit() else 0 for part in parts]
    
    # Ensure three components
    return parts + [0] * (3 - len(parts))

def find_newer_version(current_version, tags):
    """
    Finds the newest version from the tag list compared to the current version.
    """
    current_major, current_minor, current_patch = parse_version(current_version)

    def tag_precedence(tag):
        """
        Assign precedence value to tags for proper comparison.
        """
        tag_major, tag_minor, tag_patch = parse_version(tag['name'])
        return (tag_major, tag_minor, tag_patch, -tag.get('type', 3))

    # Sort tags by major, minor, patch, and type (type indicates rc, beta, etc.)
    sorted_tags = sorted(tags, key=tag_precedence, reverse=True)
    
    for tag in sorted_tags:
        tag_major, tag_minor, tag_patch = parse_version(tag['name'])
        
        if (tag_major > current_major or
            (tag_major == current_major and tag_minor > current_minor) or
            (tag_major == current_major and tag_minor == current_minor and tag_patch > current_patch)):
            return tag['name']
    
    return current_version

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
    Processes the version files, updating them with the latest GitLab tags.
    """
    try:
        for project_name in os.listdir(version_dir):
            project_version = get_version_from_file(project_name)
            if not project_version:
                print(f"Skipping {project_name} due to missing version.")
                continue

            tags = get_tags_from_gitlab(f"https://gitlab.gnome.org/{project_name}")
            if tags:
                newer_version = find_newer_version(project_version, tags)
                if newer_version != project_version:
                    print(f"Updating version for {project_name}: {project_version} -> {newer_version}")
                    update_version_file(project_name, newer_version)
                else:
                    print(f"Version for {project_name} is already up-to-date.")
            else:
                print(f"No tags found for {project_name}.")

    except Exception as e:
        print(f"Error processing version files: {e}")

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
