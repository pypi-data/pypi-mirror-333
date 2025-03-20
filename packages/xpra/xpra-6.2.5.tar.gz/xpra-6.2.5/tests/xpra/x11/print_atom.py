# This file is part of Xpra.
# Copyright (C) 2012-2022 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

import sys

from xpra.util.str_fn import bytestostr
from xpra.x11.gtk import gdk_display_source  #@UnresolvedImport, @Reimport

gdk_display_source.init_gdk_display_source()  # @UndefinedVariable

from xpra.x11.bindings.window import X11WindowBindings  #@UnresolvedImport

X11Window = X11WindowBindings()

for s in sys.argv[1:]:
    if s.lower().startswith("0x"):
        v = int(s, 16)
    else:
        v = int(s)
    print("%s : %s" % (s, bytestostr(X11Window.XGetAtomName(v))))
