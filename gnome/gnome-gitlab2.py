#!/usr/bin/env python3

import os
import sys
import re
import urllib.parse
import requests
from datetime import datetime, timedelta
import pytz  # Required for timezone handling


def print_debug(message):
    """Helper function to print debug messages."""
    print(f"[DEBUG] {message}")


def parse_version(version_str):
    """Parses a version string and extracts version numbers."""
    version_match = re.search(r'(\d+)[._](\d+)(?:[._](\d+))?', version_str)
    if version_match:
        major = int(version_match.group(1))
        minor = int(version_match.group(2))
        patch = int(version_match.group(3)) if version_match.group(3) else 0
        return major, minor, patch
    else:
        raise ValueError(f"Invalid version format: {version_str}")


def format_version(major, minor, patch=0):
    """Formats version components into a string."""
    if patch > 0:
        return f"{major}.{minor}.{patch}"
    return f"{major}.{minor}"


def get_tags_from_gitlab(repo_url, access_token=None, suppress_404=True, current_version=None):
    """
    Fetches all tags from a GitLab repository without cloning it, filtering out tags older than 9 months,
    but considering tags up to 3 years ago as valid if no tags are within the last 9 months.
    Prints the download URLs for the tags found.
    Optionally, only shows the tag matching the current version.
    """
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

        headers = {}
        if access_token:
            headers["Private-Token"] = access_token

        response = requests.get(tags_url, headers=headers)

        if response.status_code == 200:
            print_debug(f"Successfully fetched tags from {repo_url}")
            tags = response.json()

            nine_months_ago = datetime.now(pytz.utc) - timedelta(days=9 * 30)
            three_years_ago = datetime.now(pytz.utc) - timedelta(days=3 * 365)

            recent_tags = [
                tag for tag in tags
                if datetime.strptime(tag['commit']['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z") > nine_months_ago
            ]

            if not recent_tags:
                recent_tags = [
                    tag for tag in tags
                    if datetime.strptime(tag['commit']['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z") > three_years_ago
                ]

            if current_version:
                for tag in recent_tags:
                    tag_name = tag['name']
                    if tag_name == current_version:
                        download_url = f"{repo_url}/-/archive/{tag_name}/{repository_name}-{tag_name}.tar.gz"
                        print(f"Tag: {tag_name}, Download URL: {download_url}")
                        return [tag]

            else:
                for tag in recent_tags:
                    tag_name = tag['name']
                    download_url = f"{repo_url}/-/archive/{tag_name}/{repository_name}-{tag_name}.tar.gz"
                    print(f"Tag: {tag_name}, Download URL: {download_url}")

            return recent_tags

        elif response.status_code == 404:
            if not suppress_404:
                print_debug(f"Repository not found: {repo_url}. Skipping.")
            return []

        else:
            print(f"Failed to fetch tags: {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching tags: {e}")
        return []
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return []


def find_newer_version(current_version, tags):
    """Finds the newest version from the tag list compared to the current version."""
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

    if not version_dict:
        print("No valid tags found.")
        return current_version

    max_major = max(version_dict.keys())
    if max_major > current_major:
        new_version = max(version_dict[max_major], key=lambda x: (x[0], x[1]))
        return format_version(max_major, new_version[0], new_version[1])
    else:
        latest_version = current_version
        for tag_minor, tag_patch, tag_name in version_dict[current_major]:
            if (tag_minor > current_minor or
                (tag_minor == current_minor and tag_patch > current_patch)):
                formatted_version = format_version(current_major, tag_minor, tag_patch)
                if not latest_version or formatted_version > latest_version:
                    latest_version = formatted_version
    return latest_version


def process_version_files(version_dir, groups):
    """
    Processes version files and checks for updates in all specified groups.
    """
    for file in os.listdir(version_dir):
        file_path = os.path.join(version_dir, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                current_version = f.read().strip()

            project_name = file.strip()
            print_debug(f"Processing {project_name} with current version {current_version}")

            tags = []
            for group in groups:
                project_url = f"https://gitlab.gnome.org/{group}/{project_name}"
                print_debug(f"Trying {project_url}")
                group_tags = get_tags_from_gitlab(project_url)
                tags.extend(group_tags)

            if tags:
                newer_version = find_newer_version(current_version, tags)
                if newer_version != current_version:
                    print(f"Updating {project_name} from {current_version} to {newer_version}")
                    with open(file_path, 'w') as f:
                        f.write(newer_version)
            else:
                print(f"No valid tags found for {project_name} in any group.")


def main():
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
