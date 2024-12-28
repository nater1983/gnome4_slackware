#!/bin/bash

# Exit script on any error
set -e

# Toggle debug information
DEBUG=false  # Set to 'false' to disable debug information

# Array of project names and corresponding GitLab repository names
declare -A repos=(
  ["gnome-2048"]="gnome-2048"
  ["gnome-clocks"]="gnome-clocks"
  ["libspelling"]="libspelling"
  ["gtk4"]="gtk"
  ["gnome-shell"]="gnome-shell"
  ["gnome-terminal"]="gnome-terminal"
  ["gnome-control-center"]="gnome-control-center"
  ["gnome-software"]="gnome-software"
  ["gnome-contacts"]="gnome-contacts"
  ["gnome-calendar"]="gnome-calendar"
  ["gnome-photos"]="gnome-photos"
  ["gnome-maps"]="gnome-maps"
  ["gnome-weather"]="gnome-weather"
  ["gnome-system-monitor"]="gnome-system-monitor"
  ["gnome-disk-utility"]="gnome-disk-utility"
  ["gnome-text-editor"]="gnome-text-editor"
  ["mutter"]="mutter"
)

# Base GitLab URL
GITLAB_BASE_URL="https://gitlab.gnome.org/GNOME"

# Function to print debug information
debug() {
  if [[ "$DEBUG" == true ]]; then
    echo "$@"
  fi
}

# Main loop to process all repositories
for PRGNAM in "${!repos[@]}"; do
  REPO_NAME=${repos[$PRGNAM]}

  echo "Processing repository: $REPO_NAME ($PRGNAM)"

  # Use GitLab API to get the latest tag
  API_URL="https://gitlab.gnome.org/api/v4/projects/GNOME%2F${REPO_NAME}/repository/tags"
  API_RESPONSE=$(curl -s "$API_URL")
  
  # Print the API response for debugging (will be visible only if DEBUG=true)
  debug "API Response for $REPO_NAME:"
  debug "$API_RESPONSE"
  
  # Attempt to parse the latest tag
  LATEST_TAG=$(echo "$API_RESPONSE" | jq -r '.[0].name' 2>/dev/null)

  if [[ -z "$LATEST_TAG" || "$LATEST_TAG" == "null" ]]; then
    echo "Failed to fetch the latest tag for $REPO_NAME. Skipping."
    continue
  fi

  TARBALL_URL="$GITLAB_BASE_URL/$REPO_NAME/-/archive/$LATEST_TAG/$REPO_NAME-$LATEST_TAG.tar.gz"

  # Always print the following information (even if DEBUG=false)
  echo "Latest tag for $REPO_NAME: $LATEST_TAG"
  echo "Generated tarball URL: $TARBALL_URL"
  echo "SlackBuild file location: /$PRGNAM/$PRGNAM.SlackBuild"
  echo "Would replace VERSION with: $LATEST_TAG"
  echo "Would replace tarball URL with: $TARBALL_URL"
  echo "---"

  # Print debug information (will only appear if DEBUG=true)
  debug "Latest tag for $REPO_NAME: $LATEST_TAG"
  debug "Generated tarball URL: $TARBALL_URL"
  debug "SlackBuild file location: /$PRGNAM/$PRGNAM.SlackBuild"
  debug "Would replace VERSION with: $LATEST_TAG"
  debug "Would replace tarball URL with: $TARBALL_URL"
  debug "---"
done

echo "Dry run complete. No files have been modified."

