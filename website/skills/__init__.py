"""
skills init
====================================================================================================

Init script for skills sub-application

----------------------------------------------------------------------------------------------------

**Created**
    2020-04-01
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

from flask import Blueprint

app_name = "skills"
blueprint = Blueprint(app_name, __name__, url_prefix="/"+app_name)
