#!/usr/bin/python3
from sqlalchemy import Column, Integer, Sequence, String, DateTime
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """ DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """ initialize of anew bd create the engine """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """this returns a dictionary of models"""
        objects = dict()
        all_classes = (User, State, City, Amenity, Place, Review)
        if cls is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[obj_key] = obj
        return objects

    def new(self, obj):
        """Add in database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes database."""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the  session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reload from database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """ close storage"""
        self.__session.close()