#!/bin/bash
PP=python3-pycryptodomex
echo "$PP" 
cd ../../python3/python3-pycryptodomex || exit 1
bash python3-pycryptodomex.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
