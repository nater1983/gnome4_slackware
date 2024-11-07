#!/bin/bash

# Base URL and GNOME version
downloads_base_url="https://download.gnome.org/sources"

# Function to read the package version from the specified version file
get_pkg_version() {
    project_name="$1"
    version_file_path="version/$project_name"
    
    if [ -f "$version_file_path" ]; then
        cat "$version_file_path" | tr -d '\n'  # Return the version
    else
        echo "Version file for $project_name not found at $version_file_path."
        return 1
    fi
}

# Function to check if tarball is available on GNOME's downloads server
check_tarball_availability() {
    project_name="$1"
    pkg_version="$2"
    
    # Handle .0 removal for the directory path but keep it for the filename
    if [[ "$pkg_version" == *.0 ]]; then
        major_version="${pkg_version%.0}"  # Remove the last two characters ".0"
        tarball_url="$downloads_base_url/$project_name/$major_version/$project_name-$pkg_version.tar.xz"
    else
        major_version="$pkg_version"  # No change if there's no ".0"
        tarball_url="$downloads_base_url/$project_name/${major_version:0:2}/$project_name-$pkg_version.tar.xz"
    fi
    
    echo "Checking URL: $tarball_url"  # Debugging line to print the URL
    
    # Check if the tarball URL is available
    http_response=$(curl -s -o /dev/null -w "%{http_code}" "$tarball_url")
    
    if [ "$http_response" -eq 200 ]; then
        echo "$tarball_url"
    else
        echo "Error: $http_response - Tarball not found"
        return 1
    fi
}

# Function to download the tarball
download_tarball() {
    tarball_url="$1"
    target_directory="$2"
    
    tarball_name=$(basename "$tarball_url")
    tarball_path="$target_directory/$tarball_name"
    
    # Download the tarball
    curl -L -o "$tarball_path" "$tarball_url"
    
    if [ $? -eq 0 ]; then
        echo "Downloaded $tarball_name to $target_directory"
    else
        echo "Failed to download $tarball_name from $tarball_url"
    fi
}

# Main execution
if [ $# -lt 1 ]; then
    echo "Please provide a directory and project name in the format <directory>:<project_name>. Usage: ./gnome.sh <directory>:<project_name>"
    exit 1
fi

# Parse the directory and project name from the command-line argument
arg="$1"
if [[ "$arg" != *":"* ]]; then
    echo "Invalid format. Use <directory>:<project_name>."
    exit 1
fi

directory="${arg%%:*}"
project_name="${arg#*:}"

# Ensure the src directory exists for the specified project
src_directory="src/$directory"
mkdir -p "$src_directory"

# Get the package version
pkg_version=$(get_pkg_version "$project_name")

if [ $? -ne 0 ]; then
    echo "Package version not specified or version file not found, exiting."
    exit 1
fi

# Check for the tarball on the GNOME downloads server
tarball_url=$(check_tarball_availability "$project_name" "$pkg_version")

if [ $? -eq 0 ]; then
    echo "$project_name download link: $tarball_url"
    download_tarball "$tarball_url" "$src_directory"
else
    echo "Tarball for $project_name version $pkg_version not found on GNOME's downloads server."
fi

