#!/usr/bin/python3
"""Defines unittests for file_storage.py"""


import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_allfile_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_allfile(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_newfile(self):
        basem = BaseModel()
        use = User()
        statex = State()
        placex = Place()
        cityx = City()
        amen = Amenity()
        rev = Review()
        models.storage.new(basem)
        models.storage.new(use)
        models.storage.new(statex)
        models.storage.new(placex)
        models.storage.new(cityx)
        models.storage.new(amen)
        models.storage.new(rev)
        self.assertIn("BaseModel." + basem.id, models.storage.all().keys())
        self.assertIn(basem, models.storage.all().values())
        self.assertIn("User." + use.id, models.storage.all().keys())
        self.assertIn(use, models.storage.all().values())
        self.assertIn("State." + statex.id, models.storage.all().keys())
        self.assertIn(statex, models.storage.all().values())
        self.assertIn("Place." + placex.id, models.storage.all().keys())
        self.assertIn(placex, models.storage.all().values())
        self.assertIn("City." + cityx.id, models.storage.all().keys())
        self.assertIn(cityx, models.storage.all().values())
        self.assertIn("Amenity." + amen.id, models.storage.all().keys())
        self.assertIn(amen, models.storage.all().values())
        self.assertIn("Review." + rev.id, models.storage.all().keys())
        self.assertIn(rev, models.storage.all().values())

    def test_newfile_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_savefile(self):
        basem = BaseModel()
        use = User()
        statex = State()
        placex = Place()
        cityx = City()
        amen = Amenity()
        rev = Review()
        models.storage.new(basem)
        models.storage.new(use)
        models.storage.new(statex)
        models.storage.new(placex)
        models.storage.new(cityx)
        models.storage.new(amen)
        models.storage.new(rev)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + basem.id, save_text)
            self.assertIn("User." + use.id, save_text)
            self.assertIn("State." + statex.id, save_text)
            self.assertIn("Place." + placex.id, save_text)
            self.assertIn("City." + cityx.id, save_text)
            self.assertIn("Amenity." + amen.id, save_text)
            self.assertIn("Review." + rev.id, save_text)

    def test_savefile_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reloadfile(self):
        basem = BaseModel()
        use = User()
        statex = State()
        placex = Place()
        cityx = City()
        amen = Amenity()
        rev = Review()
        models.storage.new(basem)
        models.storage.new(use)
        models.storage.new(statex)
        models.storage.new(placex)
        models.storage.new(cityx)
        models.storage.new(amen)
        models.storage.new(rev)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + basem.id, objs)
        self.assertIn("User." + use.id, objs)
        self.assertIn("State." + statex.id, objs)
        self.assertIn("Place." + placex.id, objs)
        self.assertIn("City." + cityx.id, objs)
        self.assertIn("Amenity." + amen.id, objs)
        self.assertIn("Review." + rev.id, objs)

    def test_reloadfile_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


class TestFileStorage_derive(unittest.TestCase):
    """Unittests for testing the FileStorage class."""


    def test_storage_derive(self):
        self.assertEqual(type(models.storage), FileStorage)

    def test_FileStorage_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_without_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)
    
    def test_FileStorage_privatestr_path(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_privateobj_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))



if __name__ == "__main__":
    unittest.main()

