#!/bin/bash
echo Building flatpak-builder
cd ../flatpak-builder  || exit 1
source flatpak-builder.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
