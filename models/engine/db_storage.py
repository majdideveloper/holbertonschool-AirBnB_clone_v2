#!/usr/bin/python3
"""This module defines for database storage"""
from sqlalchemy import create_engine, MetaData, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """Database storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Creates engine connection"""
        from models.base_model import Base
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                      getenv('HBNB_MYSQL_USER'),
                                      getenv('HBNB_MYSQL_PWD'),
                                      getenv('HBNB_MYSQL_HOST'),
                                      getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary represent of the query"""
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.amenity import Amenity
        from models.review import Review
        from models.base_model import Base

        new_dict = {}

        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]
            for item in classes:
                result = self.__session.query(item).all()
                for element in result:
                    key = "{}.{}".format(item.__name__, element.id)
                    new_dict[key] = element
            return new_dict
        else:
            result = self.__session.query(cls).all()
            for element in result:
                key = "{}.{}".format(cls.__name__, element.id)
                new_dict[key] = element
            return new_dict

    def new(self, obj):
        """Adds the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes from the current database session"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """Creates all tables in the database"""
        from models.base_model import Base
        from models.city import City
        from models.state import State
        from models.place import Place
        from models.user import User
        from models.amenity import Amenity
        from models.review import Review

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes a session"""
        self.__session.close()
