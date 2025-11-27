#!/bin/bash
PP=python3-pykeepass
echo "$PP" 
cd ../../python3/python3-pykeepass || exit 1
bash python3-pykeepass.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
