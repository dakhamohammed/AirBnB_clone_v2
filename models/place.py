#!/usr/bin/python3
""" Place Module for HBNB project """
import shlex
from models import Amenity
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, Integer, Float, Table, ForeignKey
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


place_amenity = Table("place_amenity", Base.metadata,
                      Column("place_id", String(60),
                             ForeignKey("places.id"),
                             primary_key=True,
                             nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), nullable=False, foreign_key="cities.id")
    user_id = Column(String(60), nullable=False, foreign_key="users.id")
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="place")
        amenities = relationship("Amenity", secondary=place_amenity,
                                 viewonly=False,
                                 back_populates="place_amenities")
    else:
        @property
        def reviews(self):
            reviews_list = []
            reviews_list_to_return = []
            for key in models.storage.all():
                review = shlex.split(key.replace('.', ' '))
                if review[0] == 'Review':
                    reviews_list.append(models.storage.all(key))
            for obj in reviews_list:
                if obj.place_id == self.id:
                    reviews_list_to_return.append(obj)
            return reviews_list_to_return

        @property
        def amenities(self):
            """returns the list of Amenity instances"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, amenity_obj=None):
            """handles append method for adding an Amenity.id"""
            if type(amenity_obj) is Amenity and amenity_obj not in self.amenity_ids:
                self.amenity_ids.append(amenity_obj.id)
