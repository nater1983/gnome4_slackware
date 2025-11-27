#!/bin/bash
PP=python3-argon2-cffi
echo "$PP" 
cd ../../python3/python3-argon2-cffi || exit 1
bash python3-argon2-cffi.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
