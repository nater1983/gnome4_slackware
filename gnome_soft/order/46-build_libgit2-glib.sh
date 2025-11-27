#!/bin/bash
echo Building libgit2-glib
cd ../libgit2-glib  || exit 1
bash libgit2-glib.SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz
