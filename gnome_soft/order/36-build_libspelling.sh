#!/bin/bash
echo Building libspelling
cd ../libspelling || exit 1
bash libspelling.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
