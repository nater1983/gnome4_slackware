#!/bin/bash
PP=python3-construct
echo "$PP" 
cd ../../python3/python3-construct || exit 1
bash python3-construct.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
