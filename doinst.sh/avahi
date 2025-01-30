config() {
  NEW="$1"
  OLD="$(dirname $NEW)/$(basename $NEW .new)"
  # If there's no config file by that name, mv it over:
  if [ ! -r $OLD ]; then
    mv $NEW $OLD
  elif [ "$(cat $OLD | md5sum)" = "$(cat $NEW | md5sum)" ]; then
    # toss the redundant copy
    rm $NEW
  fi
  # Otherwise, we leave the .new copy for the admin to consider...
}

preserve_perms() {
  NEW="$1"
  OLD="$(dirname $NEW)/$(basename $NEW .new)"
  if [ -e $OLD ]; then
    cp -a $OLD ${NEW}.incoming
    cat $NEW > ${NEW}.incoming
    mv ${NEW}.incoming $NEW
  fi
  config $NEW
}


preserve_perms etc/rc.d/rc.avahidaemon.new
preserve_perms etc/rc.d/rc.avahidnsconfd.new
preserve_perms etc/avahi/avahi-daemon.conf.new

if [ -x /usr/bin/update-desktop-database ]; then
  /usr/bin/update-desktop-database -q usr/share/applications >/dev/null 2>&1
fi

# Reload messagebus service
if [ -x etc/rc.d/rc.messagebus ]; then
  chroot . /etc/rc.d/rc.messagebus reload
fi

## insertroleaccount accountname [uid] [gid]
##   This routine will create a role account on the system with the uid (and
##   optional gid) specified.  It will check to make sure that the id names
##   are not duplicated but relies on useradd and groupadd to emit errors if
##   the numeric ids would be non-unique.  Although they are optional, it is
##   recommended that the uid and gid fields be specified since Slackware
##   makes an assumption that role accounts will have ids below 100, and left
##   unspecified useradd will pick a uid above 1000.
##
insertroleaccount ()
{
  local rolename=$1 uid=$2 gid=${3:-$2}
  local tmp exists

  while read ; do
    tmp=`echo $REPLY | cut -d: -f1`
    if [ "$tmp" = "$rolename" ]; then
      exists='y'
      break
    fi
  done < $ROOT/etc/group

  if [ "$exists" != 'y' ]; then
    chroot /$ROOT /usr/sbin/groupadd ${gid:+-g $gid} $rolename
    exists='n'
  fi

  while read ; do
    tmp=`echo $REPLY | cut -d: -f1`
    if [ "$tmp" = "$rolename" ]; then
      exists='y'
      break
    fi
  done < $ROOT/etc/passwd

  if [ "$exists" != 'y' ]; then
    chroot /$ROOT /usr/sbin/useradd ${uid:+-u $uid} $rolename -g $rolename -s /bin/false -d / -c "$rolename role account"
  fi
}

insertroleaccount avahi 85 85
