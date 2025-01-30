#!/usr/bin/env python3

import os
import sys
import re
import urllib.parse
import requests
from datetime import datetime, timedelta
import pytz

def print_debug(message):
    """Helper function to print debug messages."""
    print(f"[DEBUG] {message}")

def is_stable_version(version):
    """Determines if the given version is stable."""
    return not re.search(r'-(dev|alpha|beta|rc)', version, re.IGNORECASE)

def format_version(major, minor, patch):
    """Formats version components into a string."""
    return f"{major}.{minor}.{patch}"

def parse_version(version):
    """Parses a version string into major, minor, and patch components."""
    version = version.lstrip('v').replace(',', '').strip()
    components = [c for c in version.split('.') if c.isdigit()]
    
    if len(components) < 3:
        components += ['0'] * (3 - len(components))  # Ensure at least 3 components

    try:
        return tuple(map(int, components[:3]))
    except ValueError:
        return (0, 0, 0)  # Return a safe default if parsing fails

def find_newer_version(current_version, tags):
    """Finds the newest stable version from the tag list."""
    current_version_tuple = parse_version(current_version)
    version_dict = {}

    for tag in tags:
        tag_name = tag['name']
        if not is_stable_version(tag_name):
            continue  # Skip non-stable versions

        tag_version_tuple = parse_version(tag_name)
        if tag_version_tuple[0] not in version_dict:
            version_dict[tag_version_tuple[0]] = []
        version_dict[tag_version_tuple[0]].append((tag_version_tuple, tag_name))

    if not version_dict:
        print_debug(f"No valid tags found for {current_version}. Returning current version.")
        return current_version

    max_major = max(version_dict.keys())

    if max_major > current_version_tuple[0]:
        new_version = max(version_dict[max_major], key=lambda x: x[0])
        return format_version(*new_version[0])

    latest_version = current_version_tuple
    for version_tuple, tag_name in version_dict.get(current_version_tuple[0], []):
        if version_tuple > latest_version:
            latest_version = version_tuple
            print_debug(f"Updated latest version to {format_version(*latest_version)}")

    return format_version(*latest_version)

def get_tags_from_gitlab(repo_url, access_token=None, suppress_404=True, current_version=None):
    """Fetches all tags from a GitLab repository, filtering out older tags."""
    try:
        repo_url = repo_url.strip()
        if not repo_url.startswith("https://gitlab.gnome.org/"):
            raise ValueError("The URL must start with https://gitlab.gnome.org/")

        base_api_url = "https://gitlab.gnome.org/api/v4"
        project_path = repo_url.replace("https://gitlab.gnome.org/", "").rstrip(".git")
        repository_name = project_path.split("/")[-1]

        if not project_path:
            raise ValueError("Invalid GitLab repository URL provided.")

        encoded_path = urllib.parse.quote(project_path, safe="")
        tags_url = f"{base_api_url}/projects/{encoded_path}/repository/tags"

        headers = {"Private-Token": access_token} if access_token else {}

        response = requests.get(tags_url, headers=headers, timeout=10)

        if response.status_code == 200:
            print_debug(f"Successfully fetched tags from {repo_url}")
            tags = response.json()

            nine_months_ago = datetime.now(pytz.utc) - timedelta(days=9 * 30)
            three_years_ago = datetime.now(pytz.utc) - timedelta(days=3 * 365)

            def filter_tags(tag):
                try:
                    created_at = datetime.strptime(tag['commit']['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                    return created_at > nine_months_ago or created_at > three_years_ago
                except (KeyError, ValueError):
                    return False

            recent_tags = [tag for tag in tags if filter_tags(tag)]

            if current_version:
                for tag in recent_tags:
                    if tag['name'] == current_version:
                        print(f"Tag: {tag['name']}, Download URL: {repo_url}/-/archive/{tag['name']}/{repository_name}-{tag['name']}.tar.gz")
                        return [tag]

            for tag in recent_tags:
                print(f"Tag: {tag['name']}, Download URL: {repo_url}/-/archive/{tag['name']}/{repository_name}-{tag['name']}.tar.gz")

            return recent_tags

        if response.status_code == 404 and not suppress_404:
            print_debug(f"Repository not found: {repo_url}. Skipping.")
        return []

    except (requests.RequestException, ValueError) as e:
        print_debug(f"Error fetching tags from {repo_url}: {e}")
        return []

def process_version_files(version_dir, groups):
    """Processes version files and checks for updates in all specified groups."""
    for file in os.listdir(version_dir):
        file_path = os.path.join(version_dir, file)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, 'r') as f:
            current_version = f.read().strip()

        project_name = file.strip()
        print_debug(f"Processing {project_name} with current version {current_version}")

        tags = []
        for group in groups:
            project_url = f"https://gitlab.gnome.org/{group}/{project_name}"
            print_debug(f"Trying {project_url}")
            tags.extend(get_tags_from_gitlab(project_url))

        if tags:
            newer_version = find_newer_version(current_version, tags)
            if newer_version != current_version:
                print(f"Updating {file} from {current_version} to {newer_version}")
                with open(file_path, 'w') as f:
                    f.write(newer_version)
        else:
            print(f"No valid tags found for {project_name} in any group.")

def main():
    """Main function to handle command-line arguments and execute the update process."""
    if len(sys.argv) < 3:
        print("Usage: python script.py <version_directory> <group1> [<group2> ...]")
        sys.exit(1)

    version_dir = sys.argv[1]
    groups = sys.argv[2:]

    if not os.path.isdir(version_dir):
        print(f"Error: {version_dir} is not a valid directory.")
        sys.exit(1)

    print(f"Processing versions in {version_dir} for groups: {', '.join(groups)}...")
    process_version_files(version_dir, groups)

if __name__ == "__main__":
    main()
