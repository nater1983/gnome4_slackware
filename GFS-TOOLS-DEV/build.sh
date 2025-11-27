#!/bin/bash

# gfs team 2023
# LONG LIVE SLACKWARE (1993-2023)
# updated 2024 Anagnostakis Ioannis (rizitis) GR

set -euo pipefail

# Constants
D=$(pwd)
OD=order
BD=/tmp/gfs
BL=BUILD_LOGS

# Show help function
show_help() {
    echo "Usage: $(basename "$0")"
    echo "Build scripts for Slackware packages."
    echo "This script should be run as root."
    echo "Options:"
    echo "  -h, --help     Show this help message and exit."
}

# Log function
log() {
    echo "[INFO] $(date +'%Y-%m-%d %H:%M:%S') - $*"
}

# Make scripts executable using xargs
make_scripts_executable() {
    local extension="$1"
    find . -type f -name "*.$extension" -print0 | xargs -0 chmod +x
    log "Updated permissions for all .$extension scripts."
}

# Function to log time elapsed
log_time_elapsed() {
    local log_file="$1"
    if [ -n "$log_file" ]; then
        echo "Time elapsed for $log_file: $SECONDS seconds" >> "$log_file"
    fi
    SECONDS=0
}

# Build package function
build_package() {
    local dir="$1"
    local log_file="$2"
    log "Building package in $dir..."
    
    cd "$dir" || { log "Failed to change directory to $dir"; exit 1; }
    
    if ! ./build_all.sh |& tee "$log_file"; then
        log "Warning: Build failed for $dir. Continuing to next package."
    fi
    log_time_elapsed "$log_file"
}

# Check if the script is run as root
if [ "$UID" -ne 0 ]; then
    echo "Please run this script as root."
    exit 1
fi

# Create a temporary build directory
rm -rf "$BD" || true
mkdir -p "$BD"

# Make all .SlackBuild and .sh scripts executable
make_scripts_executable "SlackBuild"
make_scripts_executable "sh"
make_scripts_executable "bash"

# Create the logs directory
mkdir -p "$D/$BL"

# Main build process
declare -A directories=(
#    [blacklist]="$D/BLACKLIST46/$OD"
    [main_gnome]="$D/main_gnome/$OD"
    [gnome]="$D/gnome/$OD"
    [gnome_soft]="$D/gnome_soft/$OD"
#    [gnome_builder]="$D/gnome_builder/$OD"
#    [extensions]="$D/extensions/$OD"
#    [backgrounds]="$D/backgrounds/$OD"
    [gnome_more]="$D/gnome_more/$OD"
#    [extras]="$D/extras/$OD"
#    [games]="$D/games/$OD"
)

# Build in the correct order for first group
for dir in blacklist main_gnome gnome; do
    if [[ -v directories[$dir] ]]; then
        build_package "${directories[$dir]}" "$D/$BL/build_${dir}.log"
    else
        log "Warning: Directory '$dir' is not defined in the directories array."
    fi
done

# Only continue on failure for the following directories
for dir in gnome_soft gnome_builder extensions backgrounds gnome_more extras games; do
    if [[ -v directories[$dir] ]]; then
        build_package "${directories[$dir]}" "$D/$BL/build_${dir}.log"
    else
        log "Warning: Directory '$dir' is not defined in the directories array."
    fi
done

# Last step
cd "$D" || { log "Failed to change directory to $D"; exit 1; }
bash configs.bash |& tee "$D/$BL/ran_configs.log"
log_time_elapsed "$D/$BL/ran_configs.log"

echo "Build process completed."
