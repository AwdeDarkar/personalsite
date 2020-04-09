"""
flask app init
====================================================================================================

By convention, the flask app is created in __init__; I restructured this code to make it a little
easier to follow by breaking distinct initialization actions into distinct functions.

----------------------------------------------------------------------------------------------------

**Created**
    2020-03-23
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


# At some point this should probably go in its own file. Maybe when there's more than one thing in
# it.
CONFIG = {
    "DATABASE": {
        "path": os.path.join("instance", "development.db.sqlite3"),
    }
}


def initialize_database(app):
    """
    Perform and needed database initializations.

    Right now this does literally nothing; database creation and migration is done through
    manage.py. However, at some point there may be other database tasks that need to be done on
    every startup of the application and this is where those would go.
    """
    from . import db
    db.init_app(app)
    return app


def initialize_login(app):
    """
    I use [flask-login](https://flask-login.readthedocs.io/en/latest/) to manage user flow,
    primarily because this is one of the places where it is easy to make mistakes that make your
    application insecure. I may rework this to use my own solution at some point, but for now the
    library does everything I need, and quite well too.
    """
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def get_user_by_id(user_id):
        return User.get_by_id(get_session(), user_id)

    return app


def initialize_blueprints(app):
    """
    Blueprints manage the url mapping. The convention I'm using is that each application is
    responsible for building its own blueprint and that blueprint must be accessible to this script.
    """
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
    if not os.getenv("FLASK_SECRET"):
        raise Exception("Flask secret key must be explicitly set as an environment variable")
    app.config.from_mapping(
        SECRET_KEY=os.getenv("FLASK_SECRET"),
        DATABASE=CONFIG["DATABASE"]["path"],
        DEBUG=os.getenv("FLASK_DEBUG", False),
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app = initialize_login(app)
    app = initialize_blueprints(app)

    return app
