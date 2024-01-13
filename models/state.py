#!/usr/bin/python3
""" Define state class """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import models
import os


class State(BaseModel, Base):
    """ Define State instance """
    __tablename__ = 'states'

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete')
    else:
        name = ""

        @property
        def cities(self):
            """
                Getter attribute cities:
                    - Return the list of City instances with state_id
                    - state_id equals to the current state_id
            """
            match_cities = []
            all_cities = models.storage.all(City).values()
            for city in all_cities:
                if city.state_id == self.id:
                    match_cities.append(city)
            return match_cities
