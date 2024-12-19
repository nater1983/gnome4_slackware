#!/bin/bash
# PP=package-name is the only value that need change for every package.
PP=libsoup3

# DO NOT edit from here untill the end, everything must be the same for every package we are building.
# If something is going wrong; then is not correct TMP= or OUTPUT= ,in ../package.SlackBuild
# These 2 vars should be in all SlackBuilds exactly like this: 
# TMP=${TMP:-./}
# OUTPUT="$CWD"
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
