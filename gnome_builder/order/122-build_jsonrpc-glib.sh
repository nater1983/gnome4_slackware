#!/bin/bash
echo Building jsonrpc-glib
cd ../jsonrpc-glib  || exit 1
source jsonrpc-glib.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
