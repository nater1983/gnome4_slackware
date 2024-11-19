import os
import sys
import urllib.parse
import requests

def print_debug(message):
    """
    Prints debug messages to the console.
    """
    print(f"[DEBUG] {message}")

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

        response = requests.get(tags_url, headers=headers)

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


def find_newer_version(current_version, tags):
    """
    Finds the newest version from the tag list compared to the current version.
    """
    def parse_version(version_str):
        parts = version_str.replace('_', '.').split('.')
        return [int(part) for part in parts] + [0] * (3 - len(parts))  # Ensure three components

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


def process_version_files(version_dir):
    """
    Cycles through all the version files in the specified directory and ensures they are updated.
    """
    for file in os.listdir(version_dir):
        file_path = os.path.join(version_dir, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                current_version = f.read().strip()

            project_name = file.strip()  # Assuming the file name corresponds to the project name

            print_debug(f"Processing {project_name} with current version {current_version}")

            project_url = f"https://gitlab.gnome.org/GNOME/{project_name}"
            tags = fetch_tags(project_url)

            if tags:
                newer_version = find_newer_version(current_version, tags)
                if newer_version != current_version:
                    print(f"Updating {file} from {current_version} to {newer_version}")
                    with open(file_path, 'w') as f:
                        f.write(newer_version)
            else:
                print(f"Failed to fetch tags for {project_name}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python t.py <version_directory>")
        sys.exit(1)

    version_dir = sys.argv[1]

    if not os.path.isdir(version_dir):
        print(f"Error: {version_dir} is not a valid directory.")
        sys.exit(1)

    print(f"Processing versions in {version_dir}...")
    process_version_files(version_dir)


if __name__ == "__main__":
    main()
