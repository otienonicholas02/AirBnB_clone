#!/usr/bin/python3
"""Defines unittests for amenity.py."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.amenity import Amenity


class TestAmenity_instantiation(unittest.TestCase):
    """Unittests for testing the Amenity class."""

    def test_string_rep(self):
        vardate = datetime.today()
        date_repr = repr(vardate)
        amen = Amenity()
        amen.id = "123456"
        amen.created_at = amen.updated_at = vardate
        amenstr = amen.__str__()
        self.assertIn("[Amenity] (123456)", amenstr)
        self.assertIn("'id': '123456'", amenstr)
        self.assertIn("'created_at': " + date_repr, amenstr)
        self.assertIn("'updated_at': " + date_repr, amenstr)

    def test_ifno_args(self):
        self.assertEqual(Amenity, type(Amenity()))

    def test_ifnew_instance_in_object(self):
        self.assertIn(Amenity(), models.storage.all().values())

    def test_ifid_public_string(self):
        self.assertEqual(str, type(Amenity().id))

    def test_ifcreated_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().created_at))

    def test_ifupdated_public_datetime(self):
        self.assertEqual(datetime, type(Amenity().updated_at))

    def test_ifname_public_class_attr(self):
        amen = Amenity()
        self.assertEqual(str, type(Amenity.name))
        self.assertIn("name", dir(Amenity()))
        self.assertNotIn("name", amen.__dict__)

    def test_if2_amenities_diff_created(self):
        amen1 = Amenity()
        sleep(0.05)
        amen2 = Amenity()
        self.assertLess(amen1.created_at, amen2.created_at)

    def test_if2_amenities_diff_updated(self):
        amen1 = Amenity()
        sleep(0.05)
        amen2 = Amenity()
        self.assertLess(amen1.updated_at, amen2.updated_at)


class TestAmenity_to_dict(unittest.TestCase):
    """Unittests for testing to_dictionery method."""

    def test_todict_type(self):
        self.assertTrue(dict, type(Amenity().to_dict()))

    def test_todict_arg(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.to_dict(None)


    def test_todict_added_attr(self):
        am = Amenity()
        am.middle_name = "Holberton"
        am.my_number = 98
        self.assertEqual("Holberton", am.middle_name)
        self.assertIn("my_number", am.to_dict())

    def test_todict_datetime_attr_strings(self):
        am = Amenity()
        am_dict = am.to_dict()
        self.assertEqual(str, type(am_dict["id"]))
        self.assertEqual(str, type(am_dict["created_at"]))
        self.assertEqual(str, type(am_dict["updated_at"]))

    def test_todict_output(self):
        dt = datetime.today()
        am = Amenity()
        am.id = "123456"
        am.created_at = am.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Amenity',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(am.to_dict(), tdict)

    def test_todict_corr_keys(self):
        am = Amenity()
        self.assertIn("id", am.to_dict())
        self.assertIn("created_at", am.to_dict())
        self.assertIn("updated_at", am.to_dict())
        self.assertIn("__class__", am.to_dict())

   

class TestAmenity_save(unittest.TestCase):
    """Unittests for testing save method."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save1(self):
        amen = Amenity()
        sleep(0.05)
        first_updated_at = amen.updated_at
        amen.save()
        self.assertLess(first_updated_at, amen.updated_at)

    def test_save2(self):
        am = Amenity()
        sleep(0.05)
        first_updated_at = am.updated_at
        am.save()
        second_updated_at = am.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        am.save()
        self.assertLess(second_updated_at, am.updated_at)

    def test_saveargs(self):
        am = Amenity()
        with self.assertRaises(TypeError):
            am.save(None)

    def test_save_updateF(self):
        am = Amenity()
        am.save()
        amid = "Amenity." + am.id
        with open("file.json", "r") as f:
            self.assertIn(amid, f.read())


if __name__ == "__main__":
    unittest.main()
