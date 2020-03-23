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
    return render_template("home.html")


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
