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


def get_engine():
    """ Get the SQLAlchemy engine connected to the database """
    try:
        if "engine" not in g:
            g.engine = create_engine("sqlite:///" + current_app.config["DATABASE"])
        return g.engine
    except RuntimeError:
        from website import CONFIG
        uri = "sqlite:///" + CONFIG["DATABASE"]["path"]
        print(f"Connecting to {uri}")
        return create_engine(uri)


def get_session():
    """ Get a fresh alchemy database session """
    if "Session" not in g:
        g.Session = sessionmaker(bind=get_engine())
    return g.Session()


def init_app(app):
    """ Perform any needed database initializations """
    pass
