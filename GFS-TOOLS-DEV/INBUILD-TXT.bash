#!/bin/bash

# Print informations for gnome-47 BUILDS.TXT for $PKG 

# Set the URL to BUILDS.TXT
url="https://reddoglinux.ddns.net/linux/gnome/47.x/source/GFSBUILDS.TXT"

# Prompt for the package name
read -p "Enter the package name: " pkg

# Download the webpage content and search for the package directory
curl -s "$url" | grep -C 12 "PRGNAM: ""$pkg"

