#!/bin/bash
echo "$(date "+%d/%m/%Y-%T")"
echo
echo
# run this script out of gnome-47 tree, like this:
# bash 47gnome-SLACKBUILDS.bash > gnome-47/SLACKBUILDS.TXT

echo
for i in `ls gnome-47/*/`; do
  NAME=$(echo $i | cut -d "/" -f2)
  LOCATION=gnome-47/*/$i
  FILES=$(ls gnome-47/*/$i)
  VERSION=$(cat gnome-47/*/$i/$i.SlackBuild | grep VERSION | grep -Eo '([0-9]+)(\.?[0-9]+)*' | head -1)
  DOWNLOAD_x86_64=$(cat gnome-47/*/$i/$i.SlackBuild |grep http | grep -o 'http.*')
  #SHA256SUM_x86_64=$(cat SUMS/$i-$VERSION.sha256sum)
  REQUIRES=$(cat gnome-47/*/$i/slack-required)
  SHORTDES=$(grep -m 1 $NAME gnome-47/*/$i/slack-desc | cut -d " " -f2-)
  echo SLACKBUILD NAME: $NAME 
  echo SLACKBUILD LOCATION: $LOCATION
  echo SLACKBUILD FILES: $FILES
  echo SLACKBUILD VERSION: $VERSION
  echo SLACKBUILD DOWNLOAD_x86_64: $DOWNLOAD_x86_64 
  echo SLACKBUILD SHA256SUM_x86_64: $SHA256SUM_x86_64
  echo SLACKBUILD REQUIRES: $REQUIRES 
  #echo PACKAGES DEPENDEES-ON: $DEPSON
  echo PACKAGE CONFLICTS:  
  echo PACKAGE SUGGESTS:  
  echo SLACKBUILD SHORT DESCRIPTION: $SHORTDES 
  echo 
done
