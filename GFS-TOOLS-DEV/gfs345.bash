#!/bin/bash
cd "$(dirname "$0")" || exit ; CWD=$(pwd)
# gfs team. 1993-2023 30 years of glory, building and rebuilding... the Universe. 
# This is our way... because...
# LONG LIVE SLACKWARE

OUTPUT_FILE="GFSBUILDS.TXT"

> "$OUTPUT_FILE"

date +"%H:%M:%S %d-%m-%y" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to process a SlackBuild script
process_build_script() {
    local build_script="$1"
    
    PRGNAM=$(awk -F= '/^PRGNAM=/{print $2}' "$build_script")
    VERSION=$(awk -F= '/^VERSION=/{print $2}' "$build_script")
    FILES=$(ls "$directory" | tr '\n' ' ')
    BUILD=$(awk -F= '/^BUILD=/{print $2}' "$build_script")
    TAG=$(awk -F= '/^TAG=/{print $2}' "$build_script")
    PKGTYPE=$(awk -F= '/^PKGTYPE=/{print $2}' "$build_script")    
    TMP=$(awk -F= '/^TMP=/{print $2}' "$build_script")
    OUTPUT=$(awk -F= '/^OUTPUT=/{print $2}' "$build_script")
    REQUIRED=$(cat "$directory"/slack-required | tr '\n' ' ')
    
    echo "" >> "$OUTPUT_FILE"


    
    echo "PRGNAM: $PRGNAM" >> "$OUTPUT_FILE"
    echo "VERSION: $VERSION" >> "$OUTPUT_FILE"
    echo "FILES: $FILES" >> "$OUTPUT_FILE"
    echo "BUILD: $BUILD" >> "$OUTPUT_FILE"
    echo "TAG: $TAG" >> "$OUTPUT_FILE"
    echo "PKGTYPE: $PKGTYPE" >> "$OUTPUT_FILE"
    echo "TMP: $TMP" >> "$OUTPUT_FILE"
    echo "OUTPUT: $OUTPUT" >> "$OUTPUT_FILE"
    echo "REQUIRED: $REQUIRED" >> "$OUTPUT_FILE"
        
    urls=$(awk '/wget\s+-c\s+http[s]?:\/\/[^\s]+/{print $NF}' "$build_script")
    if [ -n "$urls" ]; then
        echo "DOWNLOAD: $urls" >> "$OUTPUT_FILE"
    fi
}

# Function to process a directory and its contents
process_directory() {
    local directory="$1"
    local indent="$2"
    
    echo "${indent}Directory: $directory" >> "$OUTPUT_FILE"
    
    for slackbuild_file in "$directory"/*.SlackBuild; do
        if [[ -f $slackbuild_file ]]; then
            process_build_script "$slackbuild_file"
        fi
    done

    # Print a separator line after processing package information
    echo "=====================================" >> "$OUTPUT_FILE"

    for subdir in "$directory"/*; do
        if [[ -d $subdir ]]; then
            process_directory "$subdir" "$indent  "
        fi
    done
}

# Start processing from the parent directory
process_directory "../" ""

echo "GFS-BUILDS.TXT file created successfully."

