#!/bin/bash
PP=xdg-desktop-portal-gtk-gnome
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

