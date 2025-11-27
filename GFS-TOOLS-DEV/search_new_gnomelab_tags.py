import requests
from datetime import datetime, timedelta

# Define your GitLab instance and group name
gitlab_base_url = "https://gitlab.gnome.org"
group_name = "GNOME"  # Group name
activity_cutoff_days = 1  # Filter for projects active within the last ? days

# Function to get all active projects in the group
def get_all_projects():
    projects = []
    page = 1
    while True:
        # GitLab's projects API endpoint with sorting by updated_at (closest to latest activity)
        api_url = f"{gitlab_base_url}/api/v4/groups/{group_name}/projects?page={page}&per_page=100&archived=false&order_by=updated_at&sort=desc"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            print(f"Error retrieving projects: {response.status_code} - {response.text}")
            exit(1)

        page_projects = response.json()
        if not page_projects:
            break
        
        projects.extend(page_projects)
        page += 1

    return projects

# Function to get the latest tag of a project
def get_latest_tag(project_id):
    api_url = f"{gitlab_base_url}/api/v4/projects/{project_id}/repository/tags"
    response = requests.get(api_url)

    if response.status_code != 200:
        return None

    tags = response.json()
    if not tags:
        return None

    return tags[0]  # Return the most recent tag

# Get all active projects in the group
projects = get_all_projects()

# Get the current date and time in UTC
current_date = datetime.utcnow()

# Iterate through each project and print the latest tag download link for active ones
for project in projects:
    project_id = project['id']
    project_name = project['name']
    last_activity_at = project['last_activity_at']

    # Convert last activity date to a datetime object in UTC
    last_activity_date = datetime.strptime(last_activity_at, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Calculate the difference in days between the current date and the last activity date
    days_since_last_activity = (current_date - last_activity_date).days

    # Check if the project has been active within the last `activity_cutoff_days` days
    if days_since_last_activity > activity_cutoff_days:
        print(f"Skipping {project_name} due to inactivity. Last activity was {days_since_last_activity} days ago.")
        continue

    latest_tag = get_latest_tag(project_id)

    if not latest_tag:
        print(f"No tags found for project {project_name}. Skipping...")
        continue

    tag_name = latest_tag.get("name", "unknown")
    sanitized_project_name = project_name.replace(' ', '-')
    download_url = f"{gitlab_base_url}/GNOME/{sanitized_project_name}/-/archive/{tag_name}/{sanitized_project_name}-{tag_name}.tar.gz"
    print(f"{project_name} latest tag: {tag_name}")
    print(f"Download link: {download_url}\n")

