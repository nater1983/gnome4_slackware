#!/bin/bash
PP=python3-decorator
echo "$PP"
cd ../../python3/python3-decorator || exit 1
bash python3-decorator.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
