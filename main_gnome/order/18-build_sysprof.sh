#!/bin/bash
echo Building sysprof
cd ../sysprof  || exit 1
source sysprof.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
