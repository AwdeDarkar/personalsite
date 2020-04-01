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
from sassutils.wsgi import SassMiddleware
from flask_login import LoginManager

from website.db import get_db


def get_user_by_id(user_id):
    if user_id is None:
        return None
    return get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


def create_app(test_config=None):
    """
    Creates and configures the flask application
    Adapted from: <https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/>
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "development.db.sqlite3"),
        SQLALCHEMY_DATABASE_URI=os.path.join(app.instance_path, "alchemy.db.sqlite3"),
    )

    if not test_config:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    app.wsgi_app = SassMiddleware(app.wsgi_app, {
       "website": ("static/scss", "static/css", "/static/css"),
    })

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "users.login"

    @login_manager.user_loader
    def load_user(user_id):
        return get_user_by_id(user_id)

    from . import views
    app.register_blueprint(views.blueprint)

    from .auth.views import blueprint
    app.register_blueprint(blueprint)

    from .skills.views import blueprint
    app.register_blueprint(blueprint)

    return app
