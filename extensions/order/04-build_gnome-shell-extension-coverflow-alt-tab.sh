#!/bin/bash
PP=gnome-shell-extension-coverflow-alt-tab
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

