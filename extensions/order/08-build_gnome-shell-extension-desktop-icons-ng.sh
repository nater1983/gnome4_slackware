#!/bin/bash
PP=gnome-shell-extension-desktop-icons-ng
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

