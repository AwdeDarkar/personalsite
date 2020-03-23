"""
auth
====================================================================================================

Website authentication (I should have the only legal user)
Adapted from <https://flask.palletsprojects.com/en/1.1.x/tutorial/views/>

----------------------------------------------------------------------------------------------------

**Created**
    2020-03-23
**Updated**
    2020-03-23 by Ben Croisdale
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from website.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route("/", methods=("GET",))
def view_home():
    return """
    <html>
        <body>
            <h1>Ben Croisdale personal homepage</h1>
            <p>Pages:
                <ul>
                    <li><a href="/skills">Skills</a></li>
                    <li><a href="/predictions">Predictions</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </p>
        </body>
    </html>
    """


@bp.route("/skills")
def view_skills():
    return "This should list skills"


@bp.route("/predictions")
def view_predictions():
    return "This should list public predictions"


@bp.route("/about")
def view_about():
    return "This should list stuff about me"


@bp.route("/contact")
def view_contact():
    return "This should list my public contact info"
