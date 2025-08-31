#!/usr/bin/env python3

import os
import shutil

# Main source directory is fixed to /home/build
main_source_dir = "/home/build"

# Destination base directory is fixed to /mnt/www/linux
dest_base_dir = "/mnt/www/linux"

# Get user input for the subdirectory under /home/build
subdir = input("Enter the subdirectory under '/home/build': ").strip()

# Combine the main source directory with the user input
source_dir = os.path.join(main_source_dir, subdir)

# Check if the source directory exists
if not os.path.exists(source_dir):
    print(f"Source directory '{source_dir}' does not exist.")
else:
    # Get user input for the dynamic subdirectory under /mnt/www/linux
    dyn_subdir = input(f"Enter the destination subdirectory under '{dest_base_dir}': ").strip()

    # Combine base destination with user subdir
    dest_dir = os.path.join(dest_base_dir, dyn_subdir)

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

            if os.path.isfile(src_file):
                try:
                    if os.path.exists(dest_file):
                        # Ask user if they want to overwrite
                        choice = input(f"File '{dest_file}' already exists. Overwrite? (y/n): ").strip().lower()
                        if choice != "y":
                            print(f"Skipped {dest_file} (user chose not to overwrite)")
                            continue
                        # Remove existing file before moving
                        os.remove(dest_file)

                    shutil.move(src_file, dest_file)
                    moved_files.append(dest_file)
                    print(f"Moved {dest_file}")

                except Exception as e:
                    print(f"Error moving file '{src_file}': {e}")
            else:
                print(f"Skipped {filename} (not a file)")

    # Print the list of all moved .txz files
    print("\nList of moved .txz files:")
    for file in moved_files:
        print(file)

    # Delete the source directory if it's empty
    if not os.listdir(source_dir):
        os.rmdir(source_dir)
        print(f"Source directory '{source_dir}' has been deleted.")
    else:
        print(f"Source directory '{source_dir}' is not empty and was not deleted.")
