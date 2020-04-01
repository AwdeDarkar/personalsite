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

from website.db import get_session
from website import models

bp = Blueprint('auth', __name__, url_prefix='/')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = models.User.get_by_id(get_session(), user_id)


@bp.route("/", methods=("GET",))
def view_home():
    return render_template("home.html")


@bp.route("/register", methods=("GET", "POST"))
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

    return render_template('register.html')


@bp.route('/login', methods=("GET", "POST"))
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
            return redirect("/")

        flash(error)

    return render_template('login.html')


@bp.route("/skills")
def view_skills():
    dbsess = get_session()
    skills = dbsess.query(models.Skill)
    return render_template("skills.html", skills=skills)


@bp.route("/skills/filter/<skillname>")
def view_skill_filter(skillname):
    dbsess = get_session()
    skill = dbsess.query(models.Skill).filter_by(name=skillname).first()
    posts = skill.posts
    return render_template("skill_filter.html", skillname=skillname, posts=posts)


@login_required
@bp.route("/skills/create", methods=("GET", "POST"))
def view_skill_create():
    if request.method == "GET":
        return render_template("skill_create.html")
    elif request.method == "POST":
        dbsess = get_session()
        name = request.form["name"]
        skill = models.Skill(name=name)
        dbsess.add(skill)
        dbsess.commit()
        return render_template("skill_create.html")


@login_required
@bp.route("/skills/post", methods=("GET", "POST"))
def view_skill_post():
    if request.method == "GET":
        return render_template("skill_post.html")
    elif request.method == "POST":
        dbsess = get_session()
        title = request.form["title"]
        body = request.form["body"]
        post = models.Post(author_id=0, title=title, body=body)
        dbsess.add(post)
        dbsess.commit()
        return render_template("skill_post.html")


@login_required
@bp.route("/skills/link", methods=("GET", "POST"))
def view_skill_link():
    dbsess = get_session()
    posts = dbsess.query(models.Post)
    skills = dbsess.query(models.Skill)
    if request.method == "GET":
        return render_template("skill_link.html", posts=posts,
                               skills=skills)
    elif request.method == "POST":
        post_id = request.form["post_id"]
        skill_id = request.form["skill_id"]
        postskill = models.PostSkill(post_id=post_id, skill_id=skill_id)
        dbsess.add(postskill)
        dbsess.commit()
        return render_template("skill_link.html", posts=posts,
                               skills=skills)


@bp.route("/predictions")
def view_predictions():
    return render_template("predictions.html")


@bp.route("/about")
def view_about():
    return render_template("about.html")


@bp.route("/contact")
def view_contact():
    return render_template("contact.html")
