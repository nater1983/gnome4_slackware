#!/bin/bash
PP=python3-zxcvbn
echo "$PP" 
cd ../../python3/python3-zxcvbn || exit 1
bash python3-zxcvbn.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
