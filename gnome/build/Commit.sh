#!/bin/bash
# -----------------------------------------------------------------------------
# Purpose: A script to checkout latest tag from GNOME Git repositories and
# create versioned tarballs of them.
# Author:  Adapted for GNOME
# Date:    20240101 (Updated 2025-05-16)
# -----------------------------------------------------------------------------

# Defaults:

# Directory where we start:
CWD=$(pwd)

# Cleanup (delete) the directories containing the local clones afterwards:
CLEANUP="YES"

# Forced overwriting of existing tarballs:
FORCE="NO"

# Where to write the files by default:
MYDIR="${CWD}/src"

# GNOME Git repositories base URL:
GNOMEGITURI="hhttps://github.com/sonnyp/"

# Default list of modules to checkout:
DEFMODS="Commit"

# Shrink the tarball by removing git repository metadata:
SHRINK="YES"

# The GNOME topdirectory (by default the location of this script):
TOPDIR=$(cd "$(dirname "$0")"; pwd)

# ----------------------------------------------------------------------------
while getopts "cfgo:" Option
do
  case $Option in
    c ) CLEANUP="YES" ;;
    f ) FORCE="YES" ;;
    g ) SHRINK="NO" ;;
    o ) MYDIR="$(cd "${OPTARG}" && pwd)" ;;
    h|* )
      echo "$(basename "$0") [<param> <param> ...] [<module> <module> ...]"
      echo "Parameters are:"
      echo "  -c            Cleanup afterwards (delete the cloned repos)."
      echo "  -f            Force overwriting of tarballs if they exist."
      echo "  -g            Keep git repository metadata (bigger tarball)."
      echo "  -o <dir>      Create tarballs in <dir> instead of $MYDIR/."
      exit 0
      ;;
  esac
done

shift $((OPTIND - 1))

# All remaining arguments are module names
MODS="${@:-$DEFMODS}"

# Verify that our TOPDIR is the GNOME source top directory:
if ! [ -d "${TOPDIR}/src" ]; then
  echo ">> Error: '$TOPDIR' does not seem to contain the GNOME source directory"
  echo ">> Either place this script in the GNOME directory before running it,"
  echo ">> Or specify the GNOME toplevel source directory with the '-o' parameter"
  exit 1
fi

# Create the output directory:
mkdir -p "${MYDIR}" || {
  echo "Error creating '${MYDIR}' - aborting."
  exit 1
}

cd "${MYDIR}"

echo ">> Checking out the sources..."
for LOC in $MODS; do
  echo ">>   Fetching ${LOC} from ${GNOMEGITURI}..."

  # Clone the repository
  git clone --quiet "${GNOMEGITURI}${LOC}.git" "${LOC}-temp"
  if [ $? -ne 0 ]; then
    echo ">>     Failed to clone ${LOC}."
    continue
  fi

  cd "${LOC}-temp" || continue

  # Fetch tags and get the latest
  LATEST_TAG=$(git describe --tags "$(git rev-list --tags --max-count=1)" 2>/dev/null)
  if [ -z "$LATEST_TAG" ]; then
    echo ">>     No tags found for ${LOC}, skipping."
    cd ..
    rm -rf "${LOC}-temp"
    continue
  fi

  git checkout --quiet "$LATEST_TAG"
  SHORT_HASH=$(git rev-parse --short HEAD)
  VERSION="${LATEST_TAG}.${SHORT_HASH}"
  cd ..

  # Rename the directory using version info
  NEW_DIR="${LOC}-${VERSION}"
  mv "${LOC}-temp" "${NEW_DIR}"

  # Remove git metadata if SHRINK is enabled
  if [ "$SHRINK" = "YES" ]; then
    echo ">>     Removing git metadata from ${NEW_DIR}..."
    find "${NEW_DIR}" -name ".git*" -depth -exec rm -rf {} +
  fi

  # Create tarball
  echo ">>     Creating tarball for ${NEW_DIR}..."
  if [ "$FORCE" = "NO" ] && [ -f "${NEW_DIR}.tar.xz" ]; then
    echo ">>     Tarball '${NEW_DIR}.tar.xz' already exists. Use -f to overwrite."
  else
    tar -Jcf "${NEW_DIR}.tar.xz" "${NEW_DIR}"
  fi

  # Cleanup if specified
  if [ "$CLEANUP" = "YES" ]; then
    echo ">>     Cleaning up ${NEW_DIR}..."
    rm -rf "${NEW_DIR}"
  fi
done

cd "$CWD"
echo ">> Done!"
