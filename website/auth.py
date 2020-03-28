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


def get_user_by_id(user_id):
    if user_id is None:
        return None
    return get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


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
    g.user = get_user_by_id(user_id)


@bp.route("/", methods=("GET",))
def view_home():
    return render_template("home.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html')


@bp.route('/login', methods=("GET", "POST"))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect("/")

        flash(error)

    return render_template('login.html')


@bp.route("/skills")
def view_skills():
    db = get_db()
    skills = db.execute("select * from skill")
    return render_template("skills.html", skills=skills)


@bp.route("/skills/filter/<skillname>")
def view_skill_filter(skillname):
    db = get_db()
    posts = db.execute(f"""select post.title, post.body from post, post_skill, skill where
    post.id = post_skill.post_id and skill.id = post_skill.skill_id and
    skill.name = "{skillname}"
    """)
    return render_template("skill_filter.html", skillname=skillname, posts=posts)


@login_required
@bp.route("/skills/create", methods=("GET", "POST"))
def view_skill_create():
    if request.method == "GET":
        return render_template("skill_create.html")
    elif request.method == "POST":
        db = get_db()
        sname = request.form["name"]
        db.execute(
            "insert into skill (name) values (?)",
            (sname,)
        )
        db.commit()
        return render_template("skill_create.html")


@login_required
@bp.route("/skills/post", methods=("GET", "POST"))
def view_skill_post():
    if request.method == "GET":
        return render_template("skill_post.html")
    elif request.method == "POST":
        db = get_db()
        ptitle = request.form["title"]
        pbody = request.form["body"]
        db.execute(
            "insert into post (author_id, title, body) values (?, ?, ?)",
            (0, ptitle, pbody)
        )
        db.commit()
        return render_template("skill_post.html")


@login_required
@bp.route("/skills/link", methods=("GET", "POST"))
def view_skill_link():
    db = get_db()
    posts = db.execute("select * from post")
    skills = db.execute("select * from skill")
    if request.method == "GET":
        return render_template("skill_link.html", posts=posts,
                               skills=skills)
    elif request.method == "POST":
        post_id = request.form["post_id"]
        skill_id = request.form["skill_id"]
        db.execute(
            "insert into post_skill (post_id, skill_id) values (?, ?)",
            (post_id, skill_id)
        )
        db.commit()
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
