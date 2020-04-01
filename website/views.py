"""
root views
====================================================================================================

Root and static page views

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

from flask import Blueprint, render_template

blueprint = Blueprint('root', __name__, url_prefix='/')


@blueprint.route("/", methods=("GET",))
def view_home():
    return render_template("home.html")


@blueprint.route("/predictions")
def view_predictions():
    return render_template("predictions.html")


@blueprint.route("/about")
def view_about():
    return render_template("about.html")


@blueprint.route("/contact")
def view_contact():
    return render_template("contact.html")
