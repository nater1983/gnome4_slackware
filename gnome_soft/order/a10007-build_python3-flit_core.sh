#!/bin/bash
PP=python3-flit_core
echo "$PP" 
cd ../../python3/python3-flit_core || exit 1
bash python3-flit_core.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
