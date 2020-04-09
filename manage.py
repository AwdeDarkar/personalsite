#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
manage
====================================================================================================

This is, somewhat transparently, inspired by django's manage.py. This gives me useful setup
procedures and other administration tasks, including a way to run the server.

I could have used flask's 'click' for this and instead opted for a more bare-bones tool that just
uses python's native 'argparse'. I may refactor later, but for now I prefer the simplicity and this
does everything I need it to.

This also doubles as a convenient reference for things I may want to do in code elsewhere.

----------------------------------------------------------------------------------------------------

**Created**
    2020-04-01
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

import argparse
import os
from getpass import getpass

from werkzeug.security import generate_password_hash

from website.db import get_session
from website.models import User


def reset_db():
    """
    Delete the existing database and use the migrations to create a new one.

    Right now this is tooled entirely for sqlite but I do not anticipate particular difficulty
    moving to a 'real' database.
    """
    if os.path.exists("instance/development.db.sqlite3"):
        print("Existing database found, deleting it")
        os.remove("instance/development.db.sqlite3")
    migrate_db()


def migrate_db():
    """
    I use alembic for migration management. Alembic is designed to work with SQLAlchemy, so this is
    a good fit for the project.

    Unfortunately, alembic, despite being a python library, seems to _really_ want to act like a
    command-line tool. Trying to directly call alembic migration stuff was causing lots of problems
    so the bodge is to just call alembic's main function directly and pass in what is needed. It
    would be nice to get tighter integrations but for now this seems to do.
    """
    from alembic import config
    print("Beginning Alembic migration")
    alembic_args = [
            "--raiseerr",
            "upgrade",
            "head"
    ]

    config.main(argv=alembic_args)
    print("Migration complete")


def make_migrations_db(message):
    """
    This is another application of alembic, it generates python scripts called "migrations". One
    nice thing about alembic is that it makes it very easy to name the migrations which makes
    management easier. The `message` arguement allows labelling migrations.
    
    One less nice thing is that alembic is far less feature-complete than django
    migratiions. At this time, it cannot detect name changes and the documentation recommends
    manually inspecting and editing (if needed) every generated migration. I'll probably need to do
    that to avoid bugs.
    """
    from alembic import config
    print("Making Alembic migrations")
    alembic_args = [
            "--raiseerr",
            "revision",
            "--autogenerate",
            "-m",
            f"\"{message}\"",
    ]

    config.main(argv=alembic_args)
    print("Migrations created")


def run_server():
    """
    This is the preferred entrypoint for the application, over the more traditional "flask run";
    it allows me to directly pass in the port and host, something that is weirdly hard to do
    elsewhere.

    Later on, if I want to do fancier stuff with multiple environments, this could be a good place
    to put some of that logic.
    """
    from website import create_app
    app = create_app()
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=os.getenv("FLASK_PORT", 5000),
    )


def insert_user():
    """
    This site is not intended for general use; visitors cannot register on their own and right now I
    am expecting the only user to be myself. This is how my user is created in deployment (which,
    yes, is a bit ugly: I will need to get onto the running instance of the server, likely a docker
    container, and run the manage command to make my user; luckily, this bit of ugliness should only
    need to happen once).
    """
    dbsess = get_session()
    username = input("Enter the admin username [default 'admin']: ") or "admin"
    user = User(username=username, password=generate_password_hash(getpass()))
    user.admin = True
    dbsess.add(user)
    dbsess.commit()
    print(f"Created admin user '{username}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Management tool for my personal website")
    parser.add_argument("action", type=str, nargs=1,
                        help="Action to perform")
    parser.add_argument("-m", type=str, nargs=1, dest="message",
                        help="Optional message", default="nomessage")

    args = parser.parse_args()
    args.action = args.action[0]

    if args.action == "reset":
        reset_db()
    elif args.action == "migrate":
        migrate_db()
    elif args.action == "makemigrations":
        make_migrations_db(args.message)
    elif args.action == "run":
        run_server()
    elif args.action == "createadmin":
        insert_user()
    else:
        print(f"Action '{args.action}' not recognized")
