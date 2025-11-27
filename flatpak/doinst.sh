#!/bin/sh
config() {
  NEW="$1"
  OLD="`dirname $NEW`/`basename $NEW .new`"
  # If there's no config file by that name, mv it over:
  if [ ! -r $OLD ]; then
    mv $NEW $OLD
  elif [ "`cat $OLD | md5sum`" = "`cat $NEW | md5sum`" ]; then # toss the redundant copy
    rm $NEW
  fi
  # Otherwise, we leave the .new copy for the admin to consider...
}
preserve_perms() {
  NEW="\$1"
  OLD="\$(dirname \$NEW)/\$(basename \$NEW .new)"
  if [ -e \$OLD ]; then
    cp -a \$OLD \${NEW}.incoming
    cat \$NEW > \${NEW}.incoming
    mv \${NEW}.incoming \$NEW
  fi
  config \$NEW
}

config etc/xdg/autostart/flatpak-autostart.desktop.new
config etc/dbus-1/system.d/org.freedesktop.Flatpak.SystemHelper.conf.new
preserve_perms etc/profile.d/flatpak.sh.new

flatpak remote-list --system &> /dev/null || :
#Adding Flatpak username and passwd
getent group flatpak >/dev/null || groupadd -r flatpak
getent passwd flatpak >/dev/null || \
useradd -r -g flatpak -d / -s /sbin/nologin \
-c "User for flatpak system helper" flatpak
flatpak remote-list --system &> /dev/null || :
