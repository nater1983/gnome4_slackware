#!/bin/bash
# -----------------------------------------------------------------------------
# Purpose: Clone latest tags from GNOME Git repos and create versioned tarballs
# Author:  Adapted for GNOME with tag cleanup
# -----------------------------------------------------------------------------

CWD=$(pwd)
CLEANUP="YES"
FORCE="NO"
MYDIR="${CWD}/src"
GNOMEGITURI="https://github.com/sonnyp/"
DEFMODS="Commit"
SHRINK="YES"
TOPDIR=$(cd "$(dirname "$0")"; pwd)

while getopts "cfgo:" Option; do
  case $Option in
    c ) CLEANUP="YES" ;;
    f ) FORCE="YES" ;;
    g ) SHRINK="NO" ;;
    o ) MYDIR="$(cd "${OPTARG}" && pwd)" ;;
    h|* )
      echo "$(basename "$0") [<param> <param> ...] [<module> <module> ...]"
      echo "  -c   Cleanup afterwards"
      echo "  -f   Force overwrite"
      echo "  -g   Keep git metadata"
      echo "  -o   Output dir"
      exit 0
      ;;
  esac
done

shift $((OPTIND - 1))
MODS="${@:-$DEFMODS}"

if ! [ -d "${TOPDIR}/src" ]; then
  echo ">> Error: '$TOPDIR' does not seem to contain the GNOME source directory"
  exit 1
fi

mkdir -p "${MYDIR}" || { echo "Error creating '${MYDIR}'"; exit 1; }

cd "${MYDIR}"
echo ">> Checking out sources..."

for LOC in $MODS; do
  echo ">>   Fetching ${LOC} from ${GNOMEGITURI}..."
  git clone --quiet "${GNOMEGITURI}${LOC}.git" "${LOC}-temp" || {
    echo ">>     Failed to clone ${LOC}"
    continue
  }

  cd "${LOC}-temp" || continue
  LATEST_TAG=$(git describe --tags "$(git rev-list --tags --max-count=1)" 2>/dev/null)

  if [ -z "$LATEST_TAG" ]; then
    echo ">>     No tags found for ${LOC}, skipping."
    cd ..
    rm -rf "${LOC}-temp"
    continue
  fi

  git checkout --quiet "$LATEST_TAG"
  # Remove leading 'v' from tag and ignore commit hash
  CLEAN_TAG="${LATEST_TAG#v}"

  cd ..
  NEW_DIR="${LOC}-${CLEAN_TAG}"
  mv "${LOC}-temp" "${NEW_DIR}"

  if [ "$SHRINK" = "YES" ]; then
    echo ">>     Removing git metadata from ${NEW_DIR}..."
    find "${NEW_DIR}" -name ".git*" -depth -exec rm -rf {} +
  fi

  echo ">>     Creating tarball for ${NEW_DIR}..."
  if [ "$FORCE" = "NO" ] && [ -f "${NEW_DIR}.tar.xz" ]; then
    echo ">>     Tarball '${NEW_DIR}.tar.xz' exists. Use -f to overwrite."
  else
    tar -Jcf "${NEW_DIR}.tar.xz" "${NEW_DIR}"
  fi

  if [ "$CLEANUP" = "YES" ]; then
    echo ">>     Cleaning up ${NEW_DIR}..."
    rm -rf "${NEW_DIR}"
  fi
done

cd "$CWD"
echo ">> Done!"
