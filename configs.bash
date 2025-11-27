#!/bin/bash

ldconfig || true
slackpkg new-config || true
updatedb
if [ -x /usr/bin/update-desktop-database ]; then
  /usr/bin/update-desktop-database -q usr/share/applications >/dev/null 2>&1
fi

if [ -x /usr/bin/update-mime-database ]; then
  /usr/bin/update-mime-database usr/share/mime >/dev/null 2>&1
fi

# If other icon themes are installed, then add to/modify this as needed
if [ -e usr/share/icons/hicolor/icon-theme.cache ]; then
  if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -f usr/share/icons/hicolor >/dev/null 2>&1
  fi
fi

if [ -e usr/share/glib-2.0/schemas ]; then
  if [ -x /usr/bin/glib-compile-schemas ]; then
    /usr/bin/glib-compile-schemas usr/share/glib-2.0/schemas >/dev/null 2>&1
  fi
fi

# clean repo from forgoten source.tar.* file...
find ./ -type f \( -name '*.tar.gz' -o -name '*.tar.xz' -o -name '*.deb' -name '*.txz' -name '*.tar.bz2' -o -name '*.zip' \) -exec rm -f {} +
echo ""
echo "Welcome to your new GNOME desktop environment on Slackware!"
echo ""
text="01010011 01101100 01100001 01100011 01101011 01110111 01100001 01110010 01100101"
smiley=";)"

color="\e[1;32m"

for ((i=0; i<${#text}; i++)); do
    echo -n -e "$color${text:$i:1}"
    sleep 0.05
done
echo ""
echo -e "\e[1;33m$smiley\e[0m"


    
    echo "************************************************************"
echo -e "  _____     _    ______ 
|  ___)   | |   \  ___)
| |      _| |_   \ \   
| |     /     \   > >  
| |    ( (| |) _ / /__ 
|_|   (_\_   _(_/_____)
          | |          
          |_|          "



