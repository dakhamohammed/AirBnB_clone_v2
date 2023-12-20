#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class Review(BaseModel):
    """ Review classto store review information """
    __tablename__ = 'reviews'
    place_id = Column(String(60), nullable=False, foreign_key='places.id')
    user_id = Column(String(60), nullable=False, foreign_key='users.id')
    text = text = Column(String(1024), nullable=False)
