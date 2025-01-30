#!/usr/bin/env python3

import os

# Define the path to the source directory
src_dir = 'src'
# Define the tarball file extensions to look for
tarball_extensions = ('.tar', '.tar.gz', '.tgz', '.tar.bz2', '.tar.xz')

def delete_tarballs(src_dir):
    # Traverse all directories under src
    for root, dirs, files in os.walk(src_dir):
        # Skip if we are in a "perm" subdirectory
        if os.path.basename(root) == 'perm':
            continue

        # Check each file in the current directory
        for file in files:
            # Check if the file has a tarball extension
            if file.endswith(tarball_extensions):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except OSError as e:
                    print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    delete_tarballs(src_dir)
