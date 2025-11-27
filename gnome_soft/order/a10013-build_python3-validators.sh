#!/bin/bash
PP=python3-validators
echo "$PP" 
cd ../../python3/python3-validators || exit 1
bash python3-validators.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
