# -*- coding: utf-8 -*-
"""
    flask
    ~~~~~
    A microframework based on Werkzeug.  It's extensively documented
    and follows best practice patterns.
    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""

import sys
from qaviton.version import __version__


if len(sys.argv) > 1:
    if sys.argv[1] == 'create':
        from qaviton.scripts import create

        if len(sys.argv) > 3:
            if 'web' in sys.argv[2]:
                create.web(sys.argv[3])
            elif 'mobile' in sys.argv[2]:
                create.web(sys.argv[3])
        elif len(sys.argv) > 2:
            if 'web' in sys.argv[2]:
                create.web()
            elif 'mobile' in sys.argv[2]:
                create.web()
            else:
                create.web(sys.argv[2])
        else:
            create.web()
