#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Class for the storage engine for serialization and de-serialization."""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Dictionary of objects."""

        return FileStorage.__objects

    def new(self, obj):
        """New object to the storage dictionary."""

        objname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(objname, obj.id)] = obj

    def reload(self):
        """De-serialization of the JSON file."""

        try:
            with open(FileStorage.__file_path) as f:
                dictobj = json.load(f)
                for o in dictobj.values():
                    classs_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(classs_name)(**o))
        except FileNotFoundError:
            return

    def save(self):
        """Serialization of the JSON file."""

        diction = FileStorage.__objects
        dictobj = {obj: diction[obj].to_dict() for obj in diction.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(dictobj, f)
