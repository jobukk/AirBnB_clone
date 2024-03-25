#!/usr/bin/python3
"""Defines Filestorage"""
import os
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """ Represent an abstracted storage engine.
    Attributes:
        __file_path (str): The name of the file to save objects to.
        __objects (dict): A dictionary of instantiated objects.
    """
    __file_path = "file.json"
    __objects = {}
    

    def all(self):
        """returns the dictionary __objects"""
        return self.__class__.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        class_name = obj.__class__.__name__
        obj_id = obj.id
        self.__class__.__objects[f"{class_name}.{obj.id}"] = obj

    def save(self):
        """Serialize __objects to the JSON file __file_path."""
        objects_dict = {}
        for key, value in self.__objects.items():
            if isinstance(value, BaseModel):
                objects_dict[key] = value.to_dict()
        with open(self.__file_path, "w") as f:
            json.dump(objects_dict, f)

    # def reload(self):
    #     """Deserialize the JSON file __file_path to __objects, if it exists"""
    #     if os.path.isfile(self.__class__.__file_path):
    #         with open(self.__class__.__file_path, "r") as json_file:
    #             self.__class__.__objects = json.load(json_file)
    def reload(self):
        """Deserialize the JSON file __file_path to __objects, if it exists"""
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            return
