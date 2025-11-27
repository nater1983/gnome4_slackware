#!/bin/bash
PP=NetworkManager-openvpn-gtk4
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

