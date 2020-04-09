"""
root views
====================================================================================================

These are the views for the main, mostly static, site pages.

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

from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required

from sqlalchemy import desc

from website.models import ContactEntry
from website.db import get_session

blueprint = Blueprint('root', __name__, url_prefix='/')


@blueprint.route("/", methods=("GET",))
def view_home():
    return render_template("home.html")


@blueprint.route("/node/<path:path>")
def view_node_modules(path):
    """ This is clunky and bad; I need it to serve React but come up with a better solution soon """
    return send_from_directory("../node_modules", path)


@blueprint.route("/predictions")
def view_predictions():
    return render_template("predictions.html")


@blueprint.route("/about")
def view_about():
    return render_template("about.html")


@blueprint.route("/messages")
@login_required
def view_messages():
    messages = get_session().query(ContactEntry).order_by(desc(ContactEntry.created_at))
    return render_template("messages.html", messages=messages)


@blueprint.route("/contact", methods=("GET", "POST"))
def view_contact():
    """
    This is the only top-level view that does anything interesting: just a simple form to dump
    messages into my database
    """
    if request.method == "POST":
        message = ContactEntry(name=request.form["name"], email=request.form["email"],
                               content=request.form["content"])
        dbsess = get_session()
        dbsess.add(message)
        dbsess.commit()
    return render_template("contact.html")
