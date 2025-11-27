#!/bin/bash
PP=atomix
echo "$PP"
cd ../"$PP"  || exit 1
source "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

