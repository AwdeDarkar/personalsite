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

from website.db import get_session
from website.models import User


def initialize_database(app):
    """ Perform and needed database initializations """
    from . import db
    db.init_app(app)
    return app


def initialize_sass(app):
    """ Setup the CSS SASS preprocessor """
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
       "website": ("static/scss", "static/css", "/static/css"),
    })
    return app


def initialize_login(app):
    """ Initialize the flask login library """
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def get_user_by_id(user_id):
        return User.get_by_id(get_session(), user_id)

    return app


def initialize_blueprints(app):
    """ Initialize the subapp URL-mapping blueprints """
    from . import views
    app.register_blueprint(views.blueprint)

    from .auth.views import blueprint
    app.register_blueprint(blueprint)

    from .skills.views import blueprint
    app.register_blueprint(blueprint)

    return app


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

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app = initialize_database(app)
    #app = initialize_sass(app)
    app = initialize_login(app)
    app = initialize_blueprints(app)

    return app
