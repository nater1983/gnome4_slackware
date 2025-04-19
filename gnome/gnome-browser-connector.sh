#!/bin/bash
# -----------------------------------------------------------------------------
# Purpose: A script to checkout sources for GNOME from the
git repositories and create versioned tarballs of them.
# Author:  Adapted for GNOME
# Date:    20240101
# -----------------------------------------------------------------------------

# Defaults:

# Directory where we start:
CWD=$(pwd)

# Cleanup (delete) the directories containing the local clones afterwards:
CLEANUP="YES"
 
# Checkout at a custom date instead of today:
CUSTDATE="NO"

# Forced overwriting of existing tarballs:
FORCE="NO"

# Where to write the files by default:
MYDIR="${CWD}/src"

# GNOME Git repositories:
GNOMEGITURI="https://github.com/GNOME/"

# Default list of modules to checkout:
DEFMODS="gnome-browser-connector"

# Preferred branch to check out from if it exists (HEAD otherwise):
DEFBRANCH="master"
#DEFBRANCH="main"

# Shrink the tarball by removing git repository metadata:
SHRINK="YES"

# Today's timestamp:
THEDATE=$(date +%Y%m%d)

# The GNOME topdirectory (by default the location of this script):
TOPDIR=$(cd $(dirname $0); pwd)

# ----------------------------------------------------------------------------
while getopts "cd:fghk:o:" Option
do
  case $Option in
    c ) CLEANUP="YES"
        ;;
    d ) THEDATE="date --date='${OPTARG}' +%Y%m%d"
        CUSTDATE="${OPTARG}"
        ;;
    f ) FORCE="YES"
        ;;
    g ) SHRINK="NO"
        ;;
    k ) TOPDIR="${OPTARG}"
        ;;
    o ) MYDIR="$(cd ${OPTARG} ; pwd)"
        ;;
    h|* ) 
        echo "$(basename $0) [<param> <param> ...] [<module> <module> ...]"
        echo "Parameters are:"
        echo "  -c            Cleanup afterwards (delete the cloned repos)."
        echo "  -d <date>     Checkout git at <date> instead of today."
        echo "  -f            Force overwriting of tarballs if they exist."
        echo "  -h            This help."
        echo "  -g            Keep git repository metadata (bigger tarball)."
        echo "  -k <dir>      Location of GNOME sources if not $(cd $(dirname $0); pwd)/."
        echo "  -o <dir>      Create tarballs in <dir> instead of $MYDIR/."
        exit
        ;;
  esac
done

shift $(($OPTIND - 1))
# End of option parsing.
#  $1 now references the first non option item supplied on the command line
#  if one exists.
# ----------------------------------------------------------------------------

# Catch any individual requests on the commandline,
# like 'gtk gnome-shell':
MODS=${1:-"${DEFMODS}"}

# Verify that our TOPDIR is the GNOME source top directory:
if ! [ -d ${TOPDIR}/src ]; then
  echo ">> Error: '$TOPDIR' does not seem to contain the GNOME source directory"
  echo ">> Either place this script in the GNOME directory before running it,"
  echo ">> Or specify the GNOME toplevel source directory with the '-k' parameter"
  exit 1
fi

# Create the work directory:
mkdir -p "${MYDIR}"
if [ $? -ne 0 ]; then
  echo "Error creating '${MYDIR}' - aborting."
  exit 1
fi
cd "${MYDIR}"

echo ">> Checking out the sources..."
for LOC in $MODS; do
  # Clone the repository:
  echo ">>   Fetching ${LOC} from ${GNOMEGITURI}..."
  git clone ${GNOMEGITURI}${LOC}.git ${LOC}-temp
  if [ $? -ne 0 ]; then
    echo ">>     Failed to checkout ${LOC}."
    continue
  fi

  # Get the latest commit date and hash
  cd ${LOC}-temp || continue
  COMMIT_INFO=$(git log --date=format:%Y%m%d --pretty=format:%cd.%h -n1)
  cd ..

  # Rename the directory with commit info
  NEW_DIR="${LOC}-${COMMIT_INFO}"
  mv ${LOC}-temp ${NEW_DIR}

  echo ">>   Checked out ${LOC} as ${NEW_DIR}"
  pushd ${NEW_DIR}
    git checkout ${DEFBRANCH}
    if [ $? -ne 0 ]; then
      BRANCH="main"
      git checkout ${BRANCH}
    fi
    if [ "$CUSTDATE" != "NO" ]; then
      # Checkout at a specified date instead of HEAD:
      git checkout $(git rev-list -n 1 --before="`date -d $THEDATE`" $BRANCH)
    fi
  popd

  # Remove git metadata if SHRINK is enabled:
  if [ "$SHRINK" = "YES" ]; then
    echo ">>     Removing git metadata..."
    find ${NEW_DIR} -name ".git*" -depth -exec rm -rf {} \;
  fi

  # Create the tarball:
  echo ">>     Creating tarball for ${LOC}..."
  if [ "$FORCE" = "NO" -a -f ${NEW_DIR}.tar.xz ]; then
    echo ">> Not overwriting existing file '${NEW_DIR}.tar.xz'"
    echo ">> Use '-f' to force overwriting existing files"
  else
    tar -Jcf ${NEW_DIR}.tar.xz ${NEW_DIR}
  fi

  # Cleanup if specified:
  if [ "$CLEANUP" = "YES" ]; then
    echo ">>     Cleaning up ${NEW_DIR}..."
    rm -rf ${NEW_DIR}
  fi
done

cd $CWD
# Done!

