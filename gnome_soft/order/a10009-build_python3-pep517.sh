#!/bin/bash
PP=python3-pep517
echo "$PP" 
cd ../../python3/python3-pep517 || exit 1
bash python3-pep517.SlackBuild 
upgradepkg --install-new --reinstall "$PP"-*.txz
