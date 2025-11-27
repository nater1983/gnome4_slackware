#!/bin/bash
PP=python3-keyring
echo "$PP"
cd ../../python3/"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE

