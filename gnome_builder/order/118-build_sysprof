#!/bin/bash
GG=$(pwd)
echo "$GG"
ln -s ../sysprof/* .
echo Building sysprof
cd ../sysprof  || exit 1
source sysprof.SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/${PRGNAM}-${VERSION}-${ARCH}-${BUILD}${TAG}.${PKGTYPE:-tgz}
cd "$GG"
find . -lname "*" -delete
echo "done"

