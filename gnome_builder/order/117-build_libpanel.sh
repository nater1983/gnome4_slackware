#!/bin/bash
echo Building libpanel
cd ../libpanel  || exit 1
source libpanel.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
