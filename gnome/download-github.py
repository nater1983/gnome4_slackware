import requests
import os

def download_tarball(repo_owner, repo_name, version_or_tag, download_dir="downloads"):
    # Check if the URL corresponds to a GitHub release format or a regular branch/tag
    if version_or_tag.startswith("v"):  # Assumption: version_or_tag for releases starts with 'v' (e.g., v1.15.10)
        # Construct the URL for the tarball hosted on GitHub Releases
        url = f"https://github.com/{repo_owner}/{repo_name}/releases/download/{version_or_tag}/{repo_name}-{version_or_tag}.tar.xz"
    else:
        # Construct the URL for the regular GitHub tarball (branch or tag format)
        url = f"https://github.com/{repo_owner}/{repo_name}/archive/{version_or_tag}/{repo_name}-{version_or_tag}.tar.gz"

    # Make a GET request to fetch the tarball
    response = requests.get(url, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Ensure the download directory exists
        os.makedirs(download_dir, exist_ok=True)

        # Define the local file path for saving the tarball
        tarball_filename = os.path.join(download_dir, f"{repo_name}-{version_or_tag}.tar.gz" if not version_or_tag.startswith("v") else f"{repo_name}-{version_or_tag}.tar.xz")
        
        # Open the file in write-binary mode and save the response content
        with open(tarball_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Tarball downloaded successfully: {tarball_filename}")
    else:
        print(f"Failed to download tarball. HTTP Status Code: {response.status_code}")

if __name__ == "__main__":
    # Get dynamic input for project details
    repo_owner = input("Enter the repository owner (e.g., hughsie): ")
    repo_name = input("Enter the repository name (e.g., appstream-glib): ")
    version_or_tag = input("Enter the version or tag (e.g., 1.15.10 or appstream_glib_0_8_3): ")
    
    # Call the function with dynamic inputs
    download_tarball(repo_owner, repo_name, version_or_tag)
