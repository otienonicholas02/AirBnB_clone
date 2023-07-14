#!/usr/bin/python3
"""All unittests for models/base_model.py."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_derive(unittest.TestCase):
    """Unittests for testing the BaseModel class."""

    
    def test_2models_unique(self):
        basem1 = BaseModel()
        basem2 = BaseModel()
        self.assertNotEqual(basem1.id, basem2.id)

    def test_2models_diff_created(self):
        basem1 = BaseModel()
        sleep(0.05)
        basem2 = BaseModel()
        self.assertLess(basem1.created_at, basem2.created_at)

    def test_2models_diff_updated(self):
        basem1 = BaseModel()
        sleep(0.05)
        basem2 = BaseModel()
        self.assertLess(basem1.updated_at, basem2.updated_at)

    def test_string_rep(self):
        datevar = datetime.today()
        date_repr = repr(datevar)
        basem = BaseModel()
        basem.id = "123456"
        basem.created_at = basem.updated_at = datevar
        bmstr = basem.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + date_repr, bmstr)
        self.assertIn("'updated_at': " + date_repr, bmstr)

    def test_forno_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_object(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_ifid_public_string(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_ifcreatedis_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_ifupdatedis_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_ifargs_notused(self):
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_with_kwargs(self):
        datevar = datetime.today()
        dat_iso = datevar.isoformat()
        basem = BaseModel(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(basem.id, "345")
        self.assertEqual(basem.created_at, datevar)
        self.assertEqual(basem.updated_at, datevar)

    
    def test_with_args_and_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        basem = BaseModel("12", id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(basem.id, "345")
        self.assertEqual(basem.created_at, dat)
        self.assertEqual(basem.updated_at, dat)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing the save method."""

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

    def test_save_arg(self):
        basem = BaseModel()
        with self.assertRaises(TypeError):
            basem.save(None)

    def test_save_update(self):
        basem = BaseModel()
        basem.save()
        bmid = "BaseModel." + basem.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())
        
    def test_1save(self):
        basem = BaseModel()
        sleep(0.05)
        first_updated_at = basem.updated_at
        basem.save()
        self.assertLess(first_updated_at, basem.updated_at)

    def test_2save(self):
        basem = BaseModel()
        sleep(0.05)
        first_updated_at = basem.updated_at
        basem.save()
        second_updated_at = basem.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        basem.save()
        self.assertLess(second_updated_at, basem.updated_at) 


class TestBaseModel_dict(unittest.TestCase):
    """Unittests for testing the to_dict method."""

    def test_for_todict_type(self):
        basem = BaseModel()
        self.assertTrue(dict, type(basem.to_dict()))

    def test_for_todict_arg(self):
        basem = BaseModel()
        with self.assertRaises(TypeError):
            basem.to_dict(None)

    def test_for_todict_added_attr(self):
        basem = BaseModel()
        basem.name = "Holberton"
        basem.my_number = 98
        self.assertIn("name", basem.to_dict())
        self.assertIn("my_number", basem.to_dict())

    def test_for_todict_rightkey(self):
        basem = BaseModel()
        self.assertIn("id", basem.to_dict())
        self.assertIn("created_at", basem.to_dict())
        self.assertIn("updated_at", basem.to_dict())
        self.assertIn("__class__", basem.to_dict())

    def test_for_todict_datetime_strings(self):
        basem = BaseModel()
        bm_dict = basem.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_for_todict_output(self):
        dt = datetime.today()
        basem = BaseModel()
        basem.id = "123456"
        basem.created_at = basem.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(basem.to_dict(), tdict)

    


if __name__ == "__main__":
    unittest.main()
