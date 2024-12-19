#!/bin/bash
PP=gnome-keyring
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

