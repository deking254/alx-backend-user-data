#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, insert, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """adds a user to the database
        """
        user_object = User()
        user_object.email = email
        user_object.hashed_password = hashed_password
        user = self._session.execute(insert(User).values(email=email,
                                     hashed_password=hashed_password))
        user_object.id = user.lastrowid
        return user_object
