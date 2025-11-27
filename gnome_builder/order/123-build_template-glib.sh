#!/bin/bash
echo Building template-glib
cd ../template-glib  || exit 1
source template-glib.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
