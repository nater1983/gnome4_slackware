#!/bin/bash
echo Building devhelp
cd ../devhelp  || exit 1
source devhelp.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
