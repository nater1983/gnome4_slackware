#!/bin/bash
echo Building gtk-vnc
cd ../gtk-vnc || exit 1
bash gtk-vnc.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
