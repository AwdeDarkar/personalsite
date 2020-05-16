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
    render_template, request, jsonify
)
from flask_login import login_required

from website import models
from website.db import get_session
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


@blueprint.route("/api", methods=("POST",))
def view_skill_api():
    """ General API for skills and posts """
    dbsess = get_session()
    action = request.form["action"]
    kind = request.form["kind"]
    if kind == "post":
        if action == "read":
            post = models.Post.get_by_id(dbsess, int(request.form["post-id"]))
            if not post:
                return "", 404
            return jsonify({
                "title": post.title,
                "content": post.body,
            })
        if action == "create":
            skills = request.form.getlist("skill-ids[]")
            post = models.Post(title=request.form["title"],
                               body=request.form["content"])
            dbsess.add(post)
            dbsess.commit()
            for skill_id in skills:
                postskill = models.PostSkill(post_id=post.id, skill_id=skill_id)
                dbsess.add(postskill)
                dbsess.commit()
            return jsonify({"new-id": post.id}), 201
        if action == "modify":
            skills = [int(_id) for _id in request.form.getlist("skill-ids[]")]
            post = models.Post.get_by_id(dbsess, int(request.form["post-id"]))
            post.title = request.form["title"]
            post.body = request.form["content"]
            dbsess.query(models.PostSkill).filter_by(post_id=post.id).delete()
            for skill_id in skills:
                postskill = models.PostSkill(post_id=post.id, skill_id=skill_id)
                dbsess.add(postskill)
                dbsess.commit()
            dbsess.add(post)
            dbsess.commit()
            return "", 202
        if action == "delete":
            pass
    if kind == "skill":
        if action == "read":
            send_skills = []
            skills = dbsess.query(models.Skill).all()
            post = models.Post.get_by_id(dbsess, int(request.form["post-id"]))
            for skill in skills:
                send_skills.append({
                    "name": skill.name,
                    "id": skill.id,
                    "selected": skill in [skl.skill for skl in post.skills] if post else False,
                })
            return jsonify({"skills": send_skills}), 200
        return "", 400
    return "", 400


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


@blueprint.route("/post", methods=("GET",))
@login_required
def view_skill_post_create():
    if request.method == "GET":
        return render_template(f"{app_name}/post.html", post_id=-1)


@blueprint.route("/post/<post_id>", methods=("GET",))
@login_required
def view_skill_post_edit(post_id):
    if request.method == "GET":
        try:
            return render_template(f"{app_name}/post.html", post_id=int(post_id))
        except ValueError:
            return "Invalid post '{post_id}'", 400


@blueprint.route("/link", methods=("GET", "POST"))
@login_required
def view_skill_link():
    """ This is unused and should probably be reviewed; the post page manages these links now """
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
