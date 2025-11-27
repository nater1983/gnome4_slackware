#!/bin/bash
echo Building d-spy
cd ../d-spy  || exit 1
source d-spy.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
