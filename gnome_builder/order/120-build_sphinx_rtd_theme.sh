#!/bin/bash
echo Building sphinx_rtd_theme
cd ../sphinx_rtd_theme  || exit 1
source sphinx_rtd_theme.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE
