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
    else:
        print(f"Action '{args.action}' not recognized")
