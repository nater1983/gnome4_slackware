#!/bin/bash
PP=python3-pyotp
echo "$PP" 
cd ../../python3/python3-pyotp || exit 1
bash python3-pyotp.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
