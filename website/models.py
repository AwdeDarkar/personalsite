"""
models
====================================================================================================

SQLAlchemy Models

----------------------------------------------------------------------------------------------------

**Created**
    2020-04-01
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SiteModel(object):
    """ Abstract site model mixin to manage common operations """

    id = Column(Integer, primary_key=True)
    """ Primary key integer ID """

    created_at = Column(DateTime, default=datetime.now)
    """ Datetime the object was created """

    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    """ Datetime the object was updated """


class User(SiteModel, Base):
    """ Site users, there should only ever by one on this site (me) """
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False)
    """ The user's unique username """

    password = Column(String, nullable=False)
    """ The user's hashed password """


class Post(SiteModel, Base):
    """ A blog post """
    __tablename__ = "post"

    title = Column(String, nullable=False)
    """ Title of the post """

    body = Column(String, default="")
    """ String blog post content """

    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    """ ID of the author of this post """

    author = relationship("User", back_populates="posts")


class Skill(SiteModel, Base):
    """ A skill (collects blog posts) """
    __tablename__ = "skill"

    name = Column(String, nullable=False)
    """ Name of the skill """


class PostSkill(SiteModel, Base):
    """ Many to Many table """
    __tablename__ = "post_skill"

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    """ Post linked to a skill """

    skill_id = Column(Integer, ForeignKey("skill.id"), nullable=False)
    """ Skill linked to a post """

    skill = relationship("Skill", back_populates="posts")

    post = relationship("Post", back_populates="skills")
