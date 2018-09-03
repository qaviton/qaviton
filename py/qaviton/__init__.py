# -*- coding: utf-8 -*-
"""
    flask
    ~~~~~
    A microframework based on Werkzeug.  It's extensively documented
    and follows best practice patterns.
    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""

__version__ = '0.0.1'


import sys


if len(sys.argv) > 1:
    if sys.argv[1] == 'create':
        from qaviton.scripts import create

        if len(sys.argv) > 3:
            if 'web' in sys.argv[2]:
                create.web(sys.argv[3])
        elif len(sys.argv) > 2:
            if 'web' in sys.argv[2]:
                create.web()
