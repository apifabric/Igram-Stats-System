# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class User(Base):
    """description: User information and authentication details."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey('profile.id'))

class Profile(Base):
    """description: Profile details of the user including their biography."""
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    bio = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

class Post(Base):
    """description: Details about user posts made on the platform."""
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

class Comment(Base):
    """description: Comments made by users on posts."""
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

class Like(Base):
    """description: Likes made by users on posts."""
    __tablename__ = 'like'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

class Follow(Base):
    """description: Defines the follow relationship between users."""
    __tablename__ = 'follow'
    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    followee_id = Column(Integer, ForeignKey('user.id'))

class Tag(Base):
    """description: Tags associated with posts."""
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

class PostTag(Base):
    """description: Associative entity for the post-to-tag relationship."""
    __tablename__ = 'post_tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('post.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))

class Message(Base):
    """description: Messages exchanged between users."""
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    sender_id = Column(Integer, ForeignKey('user.id'))
    receiver_id = Column(Integer, ForeignKey('user.id'))

class Notification(Base):
    """description: Notifications sent to users."""
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

class Log(Base):
    """description: Log of system activities."""
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True, autoincrement=True)
    entry = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Activity(Base):
    """description: User activity records."""
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    user1 = User(username="user_one", email="user1@example.com", password="hashed_pw1")
    profile1 = Profile(first_name="John", last_name="Doe", bio="Bio of John Doe", user_id=user1.id)
    post1 = Post(title="First Post", content="This is the first post content.", user_id=user1.id)
    comment1 = Comment(content="Nice post!", post_id=post1.id, user_id=user1.id)
    like1 = Like(post_id=post1.id, user_id=user1.id)
    follow1 = Follow(follower_id=user1.id, followee_id=another_user.id)
    
    
    
    session.add_all([user1, profile1, post1, comment1, like1, follow1])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
