"""
models
====================================================================================================

I use [SQLAlchemy](https://www.sqlalchemy.org/) to manage my database models. ORM is something I do
not consider optional in a web application.

Because this website is relatively database-light, I have models for all the both of my applications
in here. If this gets to be over 500 or 600 lines I will probably refactor into the subapps kinda
like django does by default.

----------------------------------------------------------------------------------------------------

**Created**
    2020-04-01
**Author**
    Ben Croisdale
**Copyright**
    This software is Free and Open Source for any purpose
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin


# This object acts to accumulate the models we define in this module
Base = declarative_base()


class SiteModel(object):
    """
    I was a bit shocked this wasn't default in SQLAlchemy, but it wasn't to hard to define on my
    own; it basically just ensures every object has a unique int id and a creation and update time.
    """

    id = Column(Integer, primary_key=True)
    """ Primary key integer ID """

    created_at = Column(DateTime, default=datetime.now)
    """ Datetime the object was created """

    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    """ Datetime the object was updated """

    @classmethod
    def get_by_id(cls, session, object_id):
        """ Query the object table and get by id """
        if object_id is None:
            return None
        return session.query(cls).filter_by(id=object_id).first()


class User(SiteModel, UserMixin, Base):
    """ Site users, there should only ever by one on this site (me) """
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False)
    """ The user's unique username """

    password = Column(String, nullable=False)
    """ The user's hashed password """

    admin = Column(Boolean, default=True)
    """ Is this user an administrator? """

    posts = relationship("Post", back_populates="author")

    @classmethod
    def get_by_name(cls, session, username):
        """ Query the user table and return the user with the name if it exists """
        user = session.query(cls).filter_by(username=username).first()
        return user


class Post(SiteModel, Base):
    """
    These are the posts in my 'skills and project' blog. For now the string is raw, but I may add a
    field to allow the post to identify itself as markdown or html or maybe something else I
    construct (probably a custom markdown extension)
    """
    __tablename__ = "post"

    title = Column(String, nullable=False)
    """ Title of the post """

    body = Column(String, default="")
    """ String blog post content """

    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    """ ID of the author of this post """

    author = relationship("User", back_populates="posts")

    skills = relationship("PostSkill", back_populates="post")


class Skill(SiteModel, Base):
    """
    'Skills' are basically tags, but with a specific idiomatic meaning: the whole point of this is
    that I can write things that will display my skills in an area and someone can just click on a
    skill and see all the stuff I've done with it.

    Future extensions probably include some way to indicate my subjective confidence in a skill, I
    may want to display things I'm still learning or things I haven't quite mastered.
    """
    __tablename__ = "skill"

    name = Column(String, nullable=False, unique=True)
    """ Name of the skill """

    posts = relationship("PostSkill", back_populates="skill")


class PostSkill(SiteModel, Base):
    """ Many to Many table joining skills and posts """
    __tablename__ = "post_skill"

    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    """ Post linked to a skill """

    skill_id = Column(Integer, ForeignKey("skill.id"), nullable=False)
    """ Skill linked to a post """

    skill = relationship("Skill", back_populates="posts")

    post = relationship("Post", back_populates="skills")


class ContactEntry(SiteModel, Base):
    """ Entry in the contact-me form """
    __tablename__ = "contact"

    name = Column(String)
    """ Name entered into the contact form """

    email = Column(String)
    """ Email entered into the contact form """

    content = Column(String)
    """ Text content entered into the contact form """
