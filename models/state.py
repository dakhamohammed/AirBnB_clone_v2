#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import models
import shlex


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade='all, delete, delete-orphan',
                          backref="state")

    @property
    def cities(self):
        obj = models.storage.all(City)
        list_of_cities = []
        return_list_of_cities = []
        for key in obj:
            list_of_cities.append(obj[key])
        for key in list_of_cities:
            if key.state.id == self.id:
                return_list_of_cities.append(key)
        return return_list_of_cities
