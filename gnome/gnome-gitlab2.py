import os
import requests
import urllib.parse
from datetime import datetime, timedelta
import pytz

# Debug function to print additional details
def print_debug(message):
    print(f"[DEBUG] {message}")

def get_tags_from_gitlab(repo_url, access_token=None):
    """
    Fetches all tags from a GitLab repository without cloning it, filtering out tags older than 9 months,
    but considering tags up to 3 years ago as valid if no tags are within the last 9 months.
    Also returns the download URL for the repository.
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
        download_url = f"{base_api_url}/projects/{encoded_path}/repository/archive.tar.gz"

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
            
            return recent_tags, download_url
        else:
            print(f"Failed to fetch tags: {response.status_code}")
            return [], None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching tags: {e}")
        return [], None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return [], None

def find_newer_version(current_version, tags):
    """
    Compares the current version with the list of tags and returns the latest tag (version).
    """
    latest_version = current_version
    for tag in tags:
        tag_version = tag['name']
        if tag_version > latest_version:
            latest_version = tag_version
    return latest_version

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

            # Fetch tags and download URL from GitLab for this project
            project_url = f"https://gitlab.gnome.org/GNOME/{project_name}"
            tags, download_url = get_tags_from_gitlab(project_url)

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
