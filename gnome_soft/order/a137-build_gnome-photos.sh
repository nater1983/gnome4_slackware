#!/bin/bash
echo Building gnome-photos
cd ../gnome-photos  || exit 1
bash gnome-photos.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
