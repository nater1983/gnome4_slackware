#!/bin/sh
#
# Description:  This script sets the environment variables G_FILENAME_ENCODING
# and G_BROKEN_FILENAMES for the glib-2.0 library.
#
# G_FILENAME_ENCODING
#       This environment variable can be set to a comma-separated list of
#       character set names.  GLib assumes that filenames are encoded in the
#       first character set from that list rather than in UTF-8.  The special
#       token "@locale" can be used to specify the character set for the
#       current locale.
#
# G_BROKEN_FILENAMES
#       If this environment variable is set, GLib assumes that filenames are
#       in the locale encoding rather than in UTF-8.

# Determine if the locale is UTF-8:
if locale charmap 2> /dev/null | grep -q UTF-8 ; then
  export G_FILENAME_ENCODING="@locale"
fi

# It doesn't hurt to export this since G_FILENAME_ENCODING takes priority
# over G_BROKEN_FILENAMES:
export G_BROKEN_FILENAMES=1
