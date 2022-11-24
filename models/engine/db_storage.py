#!/usr/bin/python3
"""This module defines a class to manage db_storage for hbnb clone"""
from sqlalchemy import create_engine

from os import getenv


from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.base_model import BaseModel, Base
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """This class manages storage of hbnb models in db_storage"""
    __engine = None
    __session = None

    def __init__(self):
        """ initialize of anew bd create the engine """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv('HBNB_MYSQL_USER'),
                                             getenv('HBNB_MYSQL_PWD'),
                                             getenv('HBNB_MYSQL_HOST'),
                                             getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.
        If cls is None, queries all types of objects.
        Return:
        Dict of queried classes in the format <class name>.<obj id> = obj."""
        if cls is None:
            objs = self.__session.query(State, City, User,
                                        Review, Place, Amenity).all()
        else:
            objs = self.__session.query(cls.__class__.__name__)
        resu = {}
        for obj in objs:
            resu[obj.__class__.__name__ + "." + obj.id] = obj
        return resu

    def new(self, obj):
        """Add obj to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)

        self.__session = Session()
