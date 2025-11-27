#!/bin/bash
PP=gnome-shell-extension-dash-to-dock
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

