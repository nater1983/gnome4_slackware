#!/bin/bash
PP=python3-prawcore
echo "$PP"
cd ../../python3/"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

