#!/usr/bin/python3
""" Import uuid & datetime modules """
from uuid import uuid4
from datetime import datetime
import models
import os
from hashlib import md5

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """ Define a BaseModel class """

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initilize a new instance of BaseModel class
        Args:
            args (tuple): Unused argument
            kwargs (dict):
        """
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.strptime(
                        value, '%Y-%m-%dT%H:%M:%S.%f'))
                    continue
                if key != '__class__':
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """
        Method to update the 'updated_at' attribute to the current time
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Method to return a dictionary representation of the BaseModel instance
        """
        dictionary = dict(self.__dict__).copy()
        dictionary['__class__'] = self.__class__.__name__
        for key, value in self.__dict__.items():
            dictionary[key] = value
            if key == 'created_at' or key == 'updated_at':
                dictionary[key] = value.isoformat()
        dictionary.pop('_sa_instance_state', None)

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            dictionary.pop('password', None)
        return dictionary

    def delete(self):
        """
            Delete the current instance from storage
        """
        models.storage.delete(self)
