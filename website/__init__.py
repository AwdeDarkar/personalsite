"""
flask app init
====================================================================================================

This script creates the flask application.

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

import os

from flask import Flask


def create_app(test_config=None):
    """
    Creates and configures the flask application
    Adapted from: <https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/>
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "development.db.sqlite3"),
    )

    if not test_config:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    # Deliver a very simple webpage, minimal requirements for v0.1
    @app.route("/test")
    def testpage():
        return "<html><body><h1>Flask up and running! You can confirm 0.1 now!"

    from . import auth
    app.register_blueprint(auth.bp)

    return app
