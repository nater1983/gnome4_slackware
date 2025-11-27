#!/bin/bash
PP=nautilus-code
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

