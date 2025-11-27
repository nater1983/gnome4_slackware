#!/bin/bash
PP=ibus-gtk4
echo "$PP"
cd ../"$PP"  || exit 1
bash ibus-gtk4.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

