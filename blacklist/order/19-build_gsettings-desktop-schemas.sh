#!/bin/bash
PP=gsettings-desktop-schemas
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

