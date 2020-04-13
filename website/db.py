"""
db
====================================================================================================

Create and manage access to site database
Adapted from <https://flask.palletsprojects.com/en/1.1.x/tutorial/database/>

----------------------------------------------------------------------------------------------------

**Created**
    2020-03-23
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import current_app, g


def _load_engine_backend(config):
    """ Load a supported backend from the engine config """
    if "active" not in config:
        raise Exception("Database config must specify an active backend!")
    active = config["active"]
    config = config[active]
    if active == "SQLITE":
        return create_engine("sqlite:///" + config["path"])
    if active == "POSTGRES":
        return create_engine(
                f"{config['dialect']}+{config['driver']}://"
                + f"{config['username']}:{config['password']}@"
                + f"{config['hostname']}:{config['hostport']}/{config['database']}")
    raise Exception(f"Unsupported backend '{active}'")


def get_engine():
    """
    Get the SQLAlchemy engine connected to the database.
    This has two formats, if we are currently inside an application then we use the app context to
    make the engine and avoid repeated connections when an already existing one is present.

    Outside an application context, the reference to `g` and `current_app` will raise a
    RuntimeError; if that happens we just create a new connection to the database ourselves. This
    makes it easy for scripts (like `manage.py`) to work with the database without having to start
    up the whole application first.
    """
    try:
        if "engine" not in g:
            g.engine = _load_engine_backend(current_app.config["DATABASE"])
        return g.engine
    except RuntimeError:
        from website import CONFIG
        return _load_engine_backend(CONFIG["DATABASE"])


def get_session():
    """
    Typically, alchemy sessions are more useful than engines. While there are a few cases where you
    want an engine and not a session, if all you're doing is working with your defined models then
    the session is what will let you actually do that.

    SQLAlchemy uses a `sessionmaker` function which you pass your engine to and it will create a
    class (or just function?) that, when instantiated, generates the actual session object itself.
    Hence why the result needs to be called.

    This, like `get_engine`, can safely fallback to a non-flask-app version outside the flask
    application context.
    """
    try:
        if "Session" not in g:
            g.Session = sessionmaker(bind=get_engine())
        return g.Session()
    except RuntimeError:
        return sessionmaker(bind=get_engine())()


def init_app(app):
    """ Perform any needed database initializations """
    pass
