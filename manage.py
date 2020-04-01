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
    from sqlalchemy import create_engine
    from website import models
    if os.path.exists("instance/development.db.sqlite3"):
        print("Existing database found, deleting it")
        os.remove("instance/development.db.sqlite3")
    engine = create_engine("sqlite:///instance/development.db.sqlite3", echo=True)
    print("Created database file; building tables")
    models.Base.metadata.create_all(engine)
    print("Built tables; database is reset")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Management tool for my personal website")
    parser.add_argument("action", type=str, nargs=1,
                        help="Action to perform")

    args = parser.parse_args()
    args.action = args.action[0]

    if args.action == "reset":
        reset_db()
    else:
        print(f"Action '{args.action}' not recognized")
