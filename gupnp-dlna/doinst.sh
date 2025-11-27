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
( cd usr/lib64 ; rm -rf libgupnp-dlna-2.0.so )
( cd usr/lib64 ; ln -sf libgupnp-dlna-2.0.so.4 libgupnp-dlna-2.0.so )
( cd usr/lib64 ; rm -rf libgupnp-dlna-2.0.so.4 )
( cd usr/lib64 ; ln -sf libgupnp-dlna-2.0.so.4.0.0 libgupnp-dlna-2.0.so.4 )
( cd usr/lib64 ; rm -rf libgupnp-dlna-gst-2.0.so )
( cd usr/lib64 ; ln -sf libgupnp-dlna-gst-2.0.so.4 libgupnp-dlna-gst-2.0.so )
( cd usr/lib64 ; rm -rf libgupnp-dlna-gst-2.0.so.4 )
( cd usr/lib64 ; ln -sf libgupnp-dlna-gst-2.0.so.4.0.0 libgupnp-dlna-gst-2.0.so.4 )
