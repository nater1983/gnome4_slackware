if [ -x /usr/bin/update-mime-database ]; then
  /usr/bin/update-mime-database /usr/share/mime &> /dev/null
fi

if [ -x /usr/bin/update-desktop-database ]; then
  /usr/bin/update-desktop-database -q usr/share/applications >/dev/null 2>&1
fi

if [ -e usr/share/icons/hicolor/icon-theme.cache ]; then
  if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache usr/share/icons/hicolor >/dev/null 2>&1
  fi
fi

if [ -e usr/share/glib-2.0/schemas ]; then
  if [ -x /usr/bin/glib-compile-schemas ]; then
    /usr/bin/glib-compile-schemas usr/share/glib-2.0/schemas >/dev/null 2>&1
  fi
fi
( cd usr/lib64 ; rm -rf librygel-core-2.6.so )
( cd usr/lib64 ; ln -sf librygel-core-2.6.so.2 librygel-core-2.6.so )
( cd usr/lib64 ; rm -rf librygel-core-2.6.so.2 )
( cd usr/lib64 ; ln -sf librygel-core-2.6.so.2.0.4 librygel-core-2.6.so.2 )
( cd usr/lib64 ; rm -rf librygel-db-2.6.so )
( cd usr/lib64 ; ln -sf librygel-db-2.6.so.2 librygel-db-2.6.so )
( cd usr/lib64 ; rm -rf librygel-db-2.6.so.2 )
( cd usr/lib64 ; ln -sf librygel-db-2.6.so.2.0.4 librygel-db-2.6.so.2 )
( cd usr/lib64 ; rm -rf librygel-renderer-2.6.so )
( cd usr/lib64 ; ln -sf librygel-renderer-2.6.so.2 librygel-renderer-2.6.so )
( cd usr/lib64 ; rm -rf librygel-renderer-2.6.so.2 )
( cd usr/lib64 ; ln -sf librygel-renderer-2.6.so.2.0.4 librygel-renderer-2.6.so.2 )
( cd usr/lib64 ; rm -rf librygel-renderer-gst-2.6.so )
( cd usr/lib64 ; ln -sf librygel-renderer-gst-2.6.so.2 librygel-renderer-gst-2.6.so )
( cd usr/lib64 ; rm -rf librygel-renderer-gst-2.6.so.2 )
( cd usr/lib64 ; ln -sf librygel-renderer-gst-2.6.so.2.0.4 librygel-renderer-gst-2.6.so.2 )
( cd usr/lib64 ; rm -rf librygel-ruih-2.0.so )
( cd usr/lib64 ; ln -sf librygel-ruih-2.0.so.1 librygel-ruih-2.0.so )
( cd usr/lib64 ; rm -rf librygel-ruih-2.0.so.1 )
( cd usr/lib64 ; ln -sf librygel-ruih-2.0.so.1.0.0 librygel-ruih-2.0.so.1 )
( cd usr/lib64 ; rm -rf librygel-server-2.6.so )
( cd usr/lib64 ; ln -sf librygel-server-2.6.so.2 librygel-server-2.6.so )
( cd usr/lib64 ; rm -rf librygel-server-2.6.so.2 )
( cd usr/lib64 ; ln -sf librygel-server-2.6.so.2.0.4 librygel-server-2.6.so.2 )
