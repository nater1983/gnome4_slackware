# GFS-tracker
Gnome For Slackware tracker

Modified script of 
```
PROJECT: gnome-info-collect
#  FILE:    client/client.py
#  LICENCE: GPLv3+
#
#  Copyright 2022 vstanek <vstanek@redhat.com>
```
to work for SysVinit and Slackware.
No uploads, no root access needed.
Just share your infos of your Slackware Gnome installation if needed or for statistics reason to help us improve it.
https://discord.gg/WzSabC7M

## INSTALL
No installation needed. Just download GFS-tracker.py and make it executable
```
chmod +x GFS-tracker.py
```
Then run it
```
python3 GFS-tracker.py
```
BUT if you want to install it
```
wget https://github.com/rizitis/GFS-tracker/archive/refs/heads/main.zip
unzip main.zip && cd GFS-tracker-main/GFS-tracker.SlackBuild/
su -c ./GFS-tracker.SlackBuild
installpkg /tmp/GFS-tracker-100-x86_64-1_rtz.tgz
```


### NOTE
script works only in Gnome Desktop and NOT as root


+-------------------------------------------------------------------------------------------------+

Slackware™ is a trademark of Patrick Volkerding. http://www.slackware.com/trademark/trademark.php

GNOME™ is trademark of the GNOME Foundation. https://foundation.gnome.org/logo-and-trademarks
