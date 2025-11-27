#!/bin/bash
echo Building gnome-builder
cd ../gnome-builder  || exit 1
source gnome-builder.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
