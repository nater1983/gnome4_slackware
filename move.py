#!/usr/bin/env python3

import os
import shutil

# Get user input for source and destination directories
source_dir = input("Enter the source directory path: ").strip()
dest_dir = input("Enter the destination directory path: ").strip()

# Check if source directory exists
if not os.path.exists(source_dir):
    print(f"Source directory '{source_dir}' does not exist.")
else:
    # Check if destination directory exists, create it if it doesn't
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"Created destination directory: {dest_dir}")

    # List to store full package names of moved files
    moved_files = []

    # Move only .txz files from the source directory to the destination directory
    for filename in os.listdir(source_dir):
        if filename.endswith(".txz"):
            src_file = os.path.join(source_dir, filename)
            dest_file = os.path.join(dest_dir, filename)
            
            # Ensure we only move files (not directories)
            if os.path.isfile(src_file):
                shutil.move(src_file, dest_file)
                moved_files.append(dest_file)  # Save full path of moved file
                print(f"Moved {dest_file}")
            else:
                print(f"Skipped {filename} (not a file)")

    # Print the list of all moved .txz files
    print("\nList of moved .txz files:")
    for file in moved_files:
        print(file)

    # Delete the source directory if it's empty
    if not os.listdir(source_dir):  # Check if source directory is now empty
        os.rmdir(source_dir)
        print(f"Source directory '{source_dir}' has been deleted.")
    else:
        print(f"Source directory '{source_dir}' is not empty and was not deleted.")
