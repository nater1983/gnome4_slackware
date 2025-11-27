#!/bin/bash
echo Building libdex
cd ../libdex  || exit 1
source libdex.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
