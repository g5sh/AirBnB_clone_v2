#!/usr/bin/python3
"""This is the place class"""
import os
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Table, Float, ForeignKey
from sqlalchemy import MetaData
from models.base_model import BaseModel, Base
import models


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'), nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), nullable=False))

class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', cascade='all, delete-orphan',
                               backref='place')
        amenities = relationship('Amenity', secondary=place_amenity,
                                 back_populates="place_amenities",
                                 viewonly=False)
    else:
        @property
        def reviews(self):
            """
            Returns a list of Review instances with specific place id
            """
            review_inst = models.storage.all(Review).values()
            all_revs = [inst for inst in review_inst\
                        if inst.place_id == self.id]
            return all_revs

        @property
        def amenities(self):
            """
            Returns a list of amenity instances
            """
            for amenity in self.amenity_ids:
                amenity_inst = models.storage.all(Amenity).values()
                all_amenities = [inst for inst in amenity_inst]
            return all_amenities

        @amenities.setter
        def amenities(self, obj_am):
            """
            set
            """
            if isinstance(obj_am, models.Amenity) == True:
                self.amenity_ids.append(obj_am.id)
