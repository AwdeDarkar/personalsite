"""
db
====================================================================================================

Create and manage access to site database
Adapted from <https://flask.palletsprojects.com/en/1.1.x/tutorial/database/>

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

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def get_engine():
    """ Get the SQLAlchemy engine connected to the database """
    if "engine" not in g:
        g.engine = create_engine("sqlite:///" + current_app.config["DATABASE"])
    return g.engine


def get_session():
    """ Get a fresh alchemy database session """
    if "Session" not in g:
        g.Session = sessionmaker(bind=get_engine())
    return g.Session()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
