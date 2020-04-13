"""
wsgi
====================================================================================================

Gunicorn WSGI entrypoint

----------------------------------------------------------------------------------------------------

**Created**
    2020-04-13
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""
from website import create_app

app = create_app()
