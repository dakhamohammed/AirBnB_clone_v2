#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """ Review classto store review information
    Attributes:
        place_id: place id.
        user_id: user id.
        text: user review text.
    """
    __tablename__ = "reviews"
    place_id = Column(String(60), nullable=False, ForeignKey("places.id"))
    user_id = Column(String(60), nullable=False, ForeignKey("places.id"))
    text = text = Column(String(1024), nullable=False)
