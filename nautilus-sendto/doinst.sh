# update glib schemas
if [ -x usr/bin/glib-compile-schemas ]; then
  usr/bin/glib-compile-schemas usr/share/glib-2.0/schemas 1> /dev/null 2> /dev/null
fi
