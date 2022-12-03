#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City
import models


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref='state', cascade="all, delete",
                              passive_deletes=True)

    @property
    def cities(self):
        """Getter of cities"""
        city_dict = models.storage.all(City)
        state_query = self.id
        list_city = []
        for key, value in city_dict.items():
            if value.state_id == self.id:
                list_city.append(value)
        return list_city
