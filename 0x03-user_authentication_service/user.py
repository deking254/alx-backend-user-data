#!/usr/bin/env python3
"""create a SQLAlchemy model named User for a database table named users"""
from sqlalchemy import (Column, INT, String, MetaData)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(INT, primary_key=True)
    email = Column(TEXT(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250))
    reset_token = Column(String(250))
