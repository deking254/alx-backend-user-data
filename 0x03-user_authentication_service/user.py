#!/usr/bin/env python3
"""create a SQLAlchemy model named User for a database table named users"""
from sqlalchemy import (create_engine, Table, Column, Integer, String, MetaData)
from  sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

engine = create_engine('mysql+mysqldb://root:@localhost/my_db')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
