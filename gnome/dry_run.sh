#!/bin/bash

# Exit script on any error
set -e

# Toggle debug information
DEBUG=false  # Set to 'true' to enable debug information

# Array of project names and corresponding GitLab repository names
declare -A repos=(
  ["amberol"]="amberol"
  ["loupe"]="loupe"
  ["gnome-tweaks"]="gnome-tweaks"
  ["gnome-backgrounds"]="gnome-backgrounds"
  ["nautilus"]="nautilus"
  ["gnome-browser-connector"]="gnome-browser-connector"
  ["xdg-desktop-portal-gnome"]="xdg-desktop-portal-gnome"
  ["gnome-menus"]="gnome-menus"
  ["gnome-autoar"]="gnome-autoar"
  ["evolution"]="evolution"
  ["evolution-data-server"]="evolution-data-server"
  ["libnma-gtk4"]="libnma"
  ["gnome-online-accounts"]="gnome-online-accounts"
  ["gtksourceview5"]="gtksourceview"
  ["geocode-glib2"]="geocode-glib"
  ["gnome-settings-daemon"]="gnome-settings-daemon"
  ["libadwaita"]="libadwaita"
  ["libgweather4"]="libgweather"
  ["gnome-bluetooth"]="gnome-bluetooth"
  ["gsound"]="gsound"
  ["librest"]="librest"
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

# Base GitLab URL for GNOME repository
GITLAB_BASE_URL="https://gitlab.gnome.org/GNOME"

# Array to store developmental release tags and their corresponding URLs
declare -A dev_releases=()

# Function to print debug information
debug() {
  if [[ "$DEBUG" == true ]]; then
    echo "$@"
  fi
}

# Function to check if a tag is older than one year
is_older_than_one_year() {
  tag_date="$1"
  current_date=$(date +%s)
  tag_timestamp=$(date -d "$tag_date" +%s)
  
  # Calculate the difference in seconds between the current date and the tag's date
  let diff=$current_date-$tag_timestamp
  let diff_days=$diff/86400

  # Check if the tag is older than 365 days (1 year)
  if (( diff_days > 365 )); then
    return 0  # Older than a year
  else
    return 1  # Not older than a year
  fi
}

# Main loop to process all repositories
for PRGNAM in "${!repos[@]}"; do
  REPO_NAME=${repos[$PRGNAM]}

  echo "Processing repository: $REPO_NAME ($PRGNAM)"

  # Check GNOME repository for all tags
  API_URL="https://gitlab.gnome.org/api/v4/projects/GNOME%2F${REPO_NAME}/repository/tags"
  debug "Checking GNOME repository: $API_URL"
  API_RESPONSE=$(curl -s -w "%{http_code}" -o response.json "$API_URL")

  # Get the HTTP status code
  HTTP_STATUS=$(tail -n 1 <<< "$API_RESPONSE")

  # Log the raw API response from GNOME
  debug "GNOME API Response: $(cat response.json)"
  
  if [[ "$HTTP_STATUS" == "404" ]]; then
    echo "GNOME API returned 404 for $REPO_NAME. Trying World repository..."

    # Check World repository if GNOME returns 404
    API_URL_WORLD="https://gitlab.gnome.org/api/v4/projects/World%2F${REPO_NAME}/repository/tags"
    debug "Checking World repository: $API_URL_WORLD"
    API_RESPONSE_WORLD=$(curl -s -w "%{http_code}" -o response_world.json "$API_URL_WORLD")

    # Get the HTTP status code for World
    HTTP_STATUS_WORLD=$(tail -n 1 <<< "$API_RESPONSE_WORLD")

    # Log the raw API response from World
    debug "World API Response: $(cat response_world.json)"

    if [[ "$HTTP_STATUS_WORLD" == "404" ]]; then
      echo "Error: 404 Not Found for $REPO_NAME in both GNOME and World repositories."
      continue
    fi

    # Parse all tags from World repository
    ALL_TAGS_WORLD=$(jq -r '.[].name' response_world.json)

    # Find the latest stable tag in World (not a developmental release)
    STABLE_TAG_WORLD=""
    for tag in $ALL_TAGS_WORLD; do
      if [[ ! "$tag" =~ (-dev|\.alpha|\.beta|\.rc) ]]; then
        STABLE_TAG_WORLD="$tag"
        break
      fi
    done

    if [[ -n "$STABLE_TAG_WORLD" ]]; then
      LATEST_TAG="$STABLE_TAG_WORLD"
      TARBALL_URL="https://gitlab.gnome.org/World/$REPO_NAME/-/archive/$LATEST_TAG/$REPO_NAME-$LATEST_TAG.tar.gz"
      echo "Found stable tag in World repository: $LATEST_TAG"
    else
      echo "Failed to fetch the latest stable tag for $REPO_NAME from World repository. Skipping."
      continue
    fi
  else
    # If GNOME does not return a 404, parse all tags from GNOME API response
    ALL_TAGS=$(jq -r '.[].name' response.json)

    # Find the latest stable tag in GNOME (not a developmental release)
    STABLE_TAG=""
    for tag in $ALL_TAGS; do
      if [[ ! "$tag" =~ (-dev|\.alpha|\.beta|\.rc) ]]; then
        STABLE_TAG="$tag"
        break
      fi
    done

    if [[ -n "$STABLE_TAG" ]]; then
      LATEST_TAG="$STABLE_TAG"
      TARBALL_URL="https://gitlab.gnome.org/GNOME/$REPO_NAME/-/archive/$LATEST_TAG/$REPO_NAME-$LATEST_TAG.tar.gz"
      echo "Found stable tag in GNOME repository: $LATEST_TAG"
    else
      echo "No valid stable tag found in GNOME for $REPO_NAME, skipping."
      continue
    fi
  fi

  # Check for and store developmental releases with a one-year limit
  for tag in $ALL_TAGS; do
    if [[ "$tag" =~ (-dev|\.alpha|\.beta|\.rc) ]]; then
      # Get the creation date of the tag (assuming we can fetch this from GitLab API)
      TAG_DATE=$(curl -s "https://gitlab.gnome.org/api/v4/projects/GNOME%2F$REPO_NAME/repository/tags/$tag" | jq -r '.commit.created_at')

      if is_older_than_one_year "$TAG_DATE"; then
        debug echo "Skipping developmental release: $tag (older than 1 year)"
      else
        dev_releases["$REPO_NAME: $tag"]="https://gitlab.gnome.org/GNOME/$REPO_NAME/-/archive/$tag/$REPO_NAME-$tag.tar.gz"
        echo "Developmental release found for $REPO_NAME: $tag"
      fi
    fi
  done

  # Print stable version info for this repository
  echo "Latest stable tag for $REPO_NAME: $LATEST_TAG"
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

# Print all collected developmental releases at the end
if [[ ${#dev_releases[@]} -gt 0 ]]; then
  echo "Developmental releases (-dev, .alpha, .beta, .rc) found:"
  for tag in "${!dev_releases[@]}"; do
    debug echo "$tag - URL: ${dev_releases[$tag]}"
  done
else
  echo "No developmental releases (-dev, .alpha, .beta, .rc) found."
fi

echo "Dry run complete. No files have been modified."
