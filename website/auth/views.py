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
    user_id = session.get('user_id')
    g.user = models.User.get_by_id(get_session(), user_id)


@blueprint.route("/register", methods=("GET", "POST"))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        dbsess = get_session()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif models.User.get_by_name(dbsess, username) is not None:
            error = f"User {username} is already registered."

        if error is None:
            user = models.User(username=username, password=generate_password_hash(password))
            dbsess.add(user)
            dbsess.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template(f"{app_name}/register.html")


@blueprint.route('/login', methods=("GET", "POST"))
def login():
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
    logout_user()
    return render_template(f"{app_name}/logout.html")
