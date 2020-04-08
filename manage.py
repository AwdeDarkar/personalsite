#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
manage
====================================================================================================

Person website management script

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
    """ Create a new sqlite database """
    if os.path.exists("instance/development.db.sqlite3"):
        print("Existing database found, deleting it")
        os.remove("instance/development.db.sqlite3")
    migrate_db()


def migrate_db():
    """ Migrate the database """
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
    """ Migrate the database """
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
    """ Run the application server """
    from website import create_app
    app = create_app()
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=os.getenv("FLASK_PORT", 5000),
    )


def insert_user():
    """ Create a new admin user """
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
