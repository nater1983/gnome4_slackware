#!/bin/bash
PP=libspelling
echo "$PP"
cd ../../../gnome_soft/"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz


