"""
auth views
====================================================================================================

Page views for auth sub-application

----------------------------------------------------------------------------------------------------

**Created**
    2020-04-01
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

from flask import (
    render_template, request, g, url_for, session, redirect, flash,
)

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, login_required

from website import models
from website.db import get_session
from website.auth import blueprint, app_name


@blueprint.before_app_request
def load_logged_in_user():
    """
    Bit of a tricky name collision here: `session` refers to the user's browser session storage,
    while `get_session` returns the alchemy session for getting the user object from the database.
    """
    user_id = session.get('user_id')
    g.user = models.User.get_by_id(get_session(), user_id)


@blueprint.route('/login', methods=("GET", "POST"))
def login():
    """
    View for logging in the user; this endpoint handles both the login page (via the GET request)
    and the actual login check and session setup.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dbsess = get_session()
        error = None
        user = models.User.get_by_name(dbsess, username)

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user.id
            login_user(user)
            if request.args and "next" in request.args:
                return redirect(request.args.get("next"))
            return redirect("/")

        flash(error)

    return render_template(f"{app_name}/login.html")


@blueprint.route('/logout')
@login_required
def logout():
    """ Simply loading the logout page while logged in will log the user out """
    logout_user()
    return render_template(f"{app_name}/logout.html")
