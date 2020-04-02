"""
skills views
====================================================================================================

Page views for skills sub-application

----------------------------------------------------------------------------------------------------

**Created**
    2020-04-01
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

from flask import (
    render_template, request
)
from flask_login import login_required

from website import models
from website.db import get_session
from website.auth.views import load_logged_in_user
from website.skills import blueprint, app_name


@blueprint.route("/")
def view_skills():
    dbsess = get_session()
    skills = dbsess.query(models.Skill)
    return render_template(f"{app_name}/skills.html", skills=skills)


@blueprint.route("/filter/<skillname>")
def view_skill_filter(skillname):
    dbsess = get_session()
    skill = dbsess.query(models.Skill).filter_by(name=skillname).first()
    postskills = skill.posts
    return render_template(f"{app_name}/filter.html", skillname=skillname, postskills=postskills)


@blueprint.route("/create", methods=("GET", "POST"))
@login_required
def view_skill_create():
    if request.method == "GET":
        return render_template(f"{app_name}/create.html")
    elif request.method == "POST":
        dbsess = get_session()
        name = request.form["name"]
        skill = models.Skill(name=name)
        dbsess.add(skill)
        dbsess.commit()
        return render_template(f"{app_name}/create.html")


@blueprint.route("/post", methods=("GET", "POST"))
@login_required
def view_skill_post():
    if request.method == "GET":
        skills = get_session().query(models.Skill).all()
        return render_template(f"{app_name}/post.html", skills=skills)
    elif request.method == "POST":
        dbsess = get_session()
        title = request.form["title"]
        body = request.form["body"]
        skills = request.form.getlist("skills")
        post = models.Post(author_id=0, title=title, body=body)
        dbsess.add(post)
        dbsess.commit()
        print(skills)
        for skill_id in skills:
            postskill = models.PostSkill(post_id=post.id, skill_id=skill_id)
            dbsess.add(postskill)
            dbsess.commit()
        return render_template(f"{app_name}/post.html")


@blueprint.route("/link", methods=("GET", "POST"))
@login_required
def view_skill_link():
    dbsess = get_session()
    posts = dbsess.query(models.Post)
    skills = dbsess.query(models.Skill)
    if request.method == "GET":
        return render_template(f"{app_name}/link.html", posts=posts,
                               skills=skills)
    elif request.method == "POST":
        post_id = request.form["post_id"]
        skill_id = request.form["skill_id"]
        postskill = models.PostSkill(post_id=post_id, skill_id=skill_id)
        dbsess.add(postskill)
        dbsess.commit()
        return render_template(f"{app_name}/link.html", posts=posts,
                               skills=skills)
