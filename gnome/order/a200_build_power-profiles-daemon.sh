#!/bin/bash
PP=power-profiles-daemon
echo "$PP"
cd ../"$PP"  || exit 1
source "$PP".SlackBuild
upgradepkg --install-new --reinstall $OUTPUT/$PRGNAM-$VERSION-$ARCH-$BUILD$TAG.$PKGTYPE

#!/bin/bash
PP=power-profiles-daemon
echo "$PP"
cd ../"$PP"  || exit 1
bash "$PP".SlackBuild
upgradepkg --install-new --reinstall "$PP"-*.txz

