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
from flask_login import LoginManager

from website.db import get_session
from website.models import User


CONFIG = {
    "DATABASE": {
        "path": os.path.join("instance", "development.db.sqlite3"),
    }
}


def initialize_database(app):
    """ Perform and needed database initializations """
    from . import db
    db.init_app(app)
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
        SECRET_KEY=os.getenv("FLASK_SECRET", "dev"),
        DATABASE=CONFIG["DATABASE"]["path"],
        DEBUG=os.getenv("FLASK_DEBUG", True),
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
    app = initialize_login(app)
    app = initialize_blueprints(app)

    return app
