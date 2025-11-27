#!/bin/bash
echo Building sysprof_344
cd ../sysprof_344  || exit 1
source sysprof.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
