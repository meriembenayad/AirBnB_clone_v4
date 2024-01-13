#!/usr/bin/python3
"""
    class serializes instances to a JSON file
    deserializes JSON file to instances
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ Private class attributes """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """ Returns the dictionary __objects """
        if cls is None:
            return self.__objects
        else:
            className = cls if isinstance(cls, str) else cls.__name__
            result_all = {}
            for key, value in self.__objects.items():
                if key.split('.')[0] == className:
                    result_all[key] = value
            return result_all

    def get(self, cls, id):
        """
            Returns the object based on the class and its ID,
            or None if not found
            Args:
                cls: class
                id: string representing the object ID
        """
        key = '{}.{}'.format(cls.__name__, id)
        return self.__objects.get(key, None)

    def count(self, cls=None):
        """
            Returns the number of objects in storage matching the given class.
            If no class is passed, returns the count of all objects in storage.
            Args:
                cls: class (optional)
        """
        if cls is None:
            return len(self.__objects)
        else:
            return len(self.all(cls))

    def new(self, obj):
        """
            Sets the obj in __objects with key:
            <obj class name>.id
        """
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """ Serializes __objects to the JSON file (path: __file_path) """
        new_dict = {}
        for key, value in FileStorage.__objects.items():
            new_dict[key] = value.to_dict().copy()

        with open(self.__file_path, mode="w", encoding="utf-8") as my_file:
            json.dump(new_dict, my_file)

    def reload(self):
        """
            deserializes the JSON file to __objects,
            (only if the JSON file (__file_path) exists;
            otherwise, do nothing.
            If the file doesn’t exist, no exception should be raised)
        """
        try:
            with open(self.__file_path, mode="r", encoding="utf-8") as my_file:
                dict_obj = json.load(my_file)

            for obj in dict_obj.values():
                cls_name = obj['__class__']
                del obj['__class__']
                class_gl = globals()[cls_name]
                inst = class_gl(**obj)
                self.new(inst)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
            delete obj from __objects if it's inside
        """
        if obj is not None:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """ call reload() method for deserializing the JSON file to objects """
        self.reload()
