#!/usr/bin/python3
""" Place Module for HBNB project """
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
    """ A place to stay
    Attributes:
        city_id: city id
        user_id: user id
        name: place name
        description: place description
        number_rooms: number of room in the place
        number_bathrooms: number of bathrooms in place
        max_guest: maximum guest number
        price_by_night:: price for one night
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), nullable=False, ForeignKey("cities.id"))
    user_id = Column(String(60), nullable=False, ForeignKey("cities.id"))
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
            """return list of review"""
            obj = models.storage.all()
            reviews_list = []
            reviews_list_to_return = []
            for key in obj:
                review_obj = key.replace('.', ' ')
                review_obj = shlex.split(review_obj)
                if review_obj[0] == 'Review':
                    reviews_list.append(obj[key])
            for val in reviews_list:
                if val.place_id == self.id:
                    reviews_list_to_return.append(val)
            return reviews_list_to_return

        @property
        def amenities(self):
            """returns the list of Amenity instances"""
            return self.amenity_ids

        @amenities.setter
        def amenities(self, obj=None):
            """handles append method for adding an Amenity.id"""
            if type(obj) is Amenity and obj.id not in self.amenity_ids:
                self.amenity_ids.append(obj.id)
