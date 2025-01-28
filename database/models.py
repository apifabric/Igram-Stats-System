# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  January 28, 2025 13:38:21
# Database: sqlite:////tmp/tmp.J8g2ctf1Rq-01JJPJ2SW2DJ7TAT1F5P21GHYS/Igram_Stats_System/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class Log(Base):  # type: ignore
    """
    description: Log of system activities.
    """
    __tablename__ = 'log'
    _s_collection_name = 'Log'  # type: ignore

    id = Column(Integer, primary_key=True)
    entry = Column(Text)
    created_at = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)



class Profile(Base):  # type: ignore
    """
    description: Profile details of the user including their biography.
    """
    __tablename__ = 'profile'
    _s_collection_name = 'Profile'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(Text)
    user_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(foreign_keys='[Profile.user_id]', back_populates=("ProfileList"))

    # child relationships (access children)
    UserList : Mapped[List["User"]] = relationship(foreign_keys='[User.profile_id]', back_populates="profile")



class Tag(Base):  # type: ignore
    """
    description: Tags associated with posts.
    """
    __tablename__ = 'tag'
    _s_collection_name = 'Tag'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    PostTagList : Mapped[List["PostTag"]] = relationship(back_populates="tag")



class User(Base):  # type: ignore
    """
    description: User information and authentication details.
    """
    __tablename__ = 'user'
    _s_collection_name = 'User'  # type: ignore

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    profile_id = Column(ForeignKey('profile.id'))

    # parent relationships (access parent)
    profile : Mapped["Profile"] = relationship(foreign_keys='[User.profile_id]', back_populates=("UserList"))

    # child relationships (access children)
    ProfileList : Mapped[List["Profile"]] = relationship(foreign_keys='[Profile.user_id]', back_populates="user")
    ActivityList : Mapped[List["Activity"]] = relationship(back_populates="user")
    FollowList : Mapped[List["Follow"]] = relationship(foreign_keys='[Follow.followee_id]', back_populates="followee")
    followerFollowList : Mapped[List["Follow"]] = relationship(foreign_keys='[Follow.follower_id]', back_populates="follower")
    MessageList : Mapped[List["Message"]] = relationship(foreign_keys='[Message.receiver_id]', back_populates="receiver")
    senderMessageList : Mapped[List["Message"]] = relationship(foreign_keys='[Message.sender_id]', back_populates="sender")
    NotificationList : Mapped[List["Notification"]] = relationship(back_populates="user")
    PostList : Mapped[List["Post"]] = relationship(back_populates="user")
    CommentList : Mapped[List["Comment"]] = relationship(back_populates="user")
    LikeList : Mapped[List["Like"]] = relationship(back_populates="user")



class Activity(Base):  # type: ignore
    """
    description: User activity records.
    """
    __tablename__ = 'activity'
    _s_collection_name = 'Activity'  # type: ignore

    id = Column(Integer, primary_key=True)
    description = Column(Text)
    user_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("ActivityList"))

    # child relationships (access children)



class Follow(Base):  # type: ignore
    """
    description: Defines the follow relationship between users.
    """
    __tablename__ = 'follow'
    _s_collection_name = 'Follow'  # type: ignore

    id = Column(Integer, primary_key=True)
    follower_id = Column(ForeignKey('user.id'))
    followee_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    followee : Mapped["User"] = relationship(foreign_keys='[Follow.followee_id]', back_populates=("FollowList"))
    follower : Mapped["User"] = relationship(foreign_keys='[Follow.follower_id]', back_populates=("followerFollowList"))

    # child relationships (access children)



class Message(Base):  # type: ignore
    """
    description: Messages exchanged between users.
    """
    __tablename__ = 'message'
    _s_collection_name = 'Message'  # type: ignore

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    sender_id = Column(ForeignKey('user.id'))
    receiver_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    receiver : Mapped["User"] = relationship(foreign_keys='[Message.receiver_id]', back_populates=("MessageList"))
    sender : Mapped["User"] = relationship(foreign_keys='[Message.sender_id]', back_populates=("senderMessageList"))

    # child relationships (access children)



class Notification(Base):  # type: ignore
    """
    description: Notifications sent to users.
    """
    __tablename__ = 'notification'
    _s_collection_name = 'Notification'  # type: ignore

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("NotificationList"))

    # child relationships (access children)



class Post(Base):  # type: ignore
    """
    description: Details about user posts made on the platform.
    """
    __tablename__ = 'post'
    _s_collection_name = 'Post'  # type: ignore

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    user : Mapped["User"] = relationship(back_populates=("PostList"))

    # child relationships (access children)
    CommentList : Mapped[List["Comment"]] = relationship(back_populates="post")
    LikeList : Mapped[List["Like"]] = relationship(back_populates="post")
    PostTagList : Mapped[List["PostTag"]] = relationship(back_populates="post")



class Comment(Base):  # type: ignore
    """
    description: Comments made by users on posts.
    """
    __tablename__ = 'comment'
    _s_collection_name = 'Comment'  # type: ignore

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    post_id = Column(ForeignKey('post.id'))
    user_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    post : Mapped["Post"] = relationship(back_populates=("CommentList"))
    user : Mapped["User"] = relationship(back_populates=("CommentList"))

    # child relationships (access children)



class Like(Base):  # type: ignore
    """
    description: Likes made by users on posts.
    """
    __tablename__ = 'like'
    _s_collection_name = 'Like'  # type: ignore

    id = Column(Integer, primary_key=True)
    post_id = Column(ForeignKey('post.id'))
    user_id = Column(ForeignKey('user.id'))

    # parent relationships (access parent)
    post : Mapped["Post"] = relationship(back_populates=("LikeList"))
    user : Mapped["User"] = relationship(back_populates=("LikeList"))

    # child relationships (access children)



class PostTag(Base):  # type: ignore
    """
    description: Associative entity for the post-to-tag relationship.
    """
    __tablename__ = 'post_tag'
    _s_collection_name = 'PostTag'  # type: ignore

    id = Column(Integer, primary_key=True)
    post_id = Column(ForeignKey('post.id'))
    tag_id = Column(ForeignKey('tag.id'))

    # parent relationships (access parent)
    post : Mapped["Post"] = relationship(back_populates=("PostTagList"))
    tag : Mapped["Tag"] = relationship(back_populates=("PostTagList"))

    # child relationships (access children)
