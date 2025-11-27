#!/bin/bash
PP=python3-typing_extensions
echo "$PP"
cd ../../../python3/"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz


