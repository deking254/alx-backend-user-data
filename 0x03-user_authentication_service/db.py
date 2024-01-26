#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine, insert, select, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def find_user_by(self, **args) -> User:
        """finds a user in the database according to the keyword argument"""
        result = self._session
        user_found = User()
        key_argument = list(args.keys())[0]
        found = False
        sql = 'select * from users where {}=:{}'.format(key_argument,
                                                        key_argument)
        try:
            a = result.execute(sql, args)
        except Exception:
            raise InvalidRequestError
        first_record = a.first()
        if first_record:
            return first_record
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **args) -> None:
        """updates the user whose id is specified"""
        user = None
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            pass
        if user is not None:
            try:
                self._session.execute(update(User).where(User.id == user_id),
                                      args)
            except Exception:
                raise ValueError
