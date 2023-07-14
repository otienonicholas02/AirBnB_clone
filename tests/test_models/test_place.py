#!/usr/bin/python3
"""Defines unittests for place.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_derive(unittest.TestCase):
    """Unittests for testing the Place class."""

    def test_ifno_args(self):
        self.assertEqual(Place, type(Place()))

    def test_ifnew_data_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_ifid_public_string(self):
        self.assertEqual(str, type(Place().id))

    def test_ifcreated_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_ifupdated_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_ifcity_id_public_class_attr(self):
        varplace = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(varplace))
        self.assertNotIn("city_id", varplace.__dict__)

    def test_ifuser_id_public_class_attr(self):
        varplace = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(varplace))
        self.assertNotIn("user_id", varplace.__dict__)

    def test_ifdescription_public_class_attr(self):
        varplace = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(varplace))
        self.assertNotIn("desctiption", varplace.__dict__)
    def test_ifname_public_class_attr(self):
        varplace = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(varplace))
        self.assertNotIn("name", varplace.__dict__)

    def test_ifnumber_rooms_public_class_attr(self):
        varplace = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(varplace))
        self.assertNotIn("number_rooms", varplace.__dict__)

    def test_ifnumber_bathrooms_public_class_attr(self):
        varplace = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(varplace))
        self.assertNotIn("number_bathrooms", varplace.__dict__)

    def test_ifmax_guest_public_class_attr(self):
        varplace = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(varplace))
        self.assertNotIn("max_guest", varplace.__dict__)

    def test_cost_per_night_public_class_attr(self):
        varplace = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(varplace))
        self.assertNotIn("price_by_night", varplace.__dict__)

    def test_latitude_public_class_attr(self):
        varplace = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(varplace))
        self.assertNotIn("latitude", varplace.__dict__)

    def test_longitude_public_class_attr(self):
        varplace = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(varplace))
        self.assertNotIn("longitude", varplace.__dict__)

    def test_amenity_public_class_attr(self):
        varplace = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(varplace))
        self.assertNotIn("amenity_ids", varplace.__dict__)

    def test_2diffplaces_unique(self):
        var1 = Place()
        var2 = Place()
        self.assertNotEqual(var1.id, var2.id)

    def test_2diffplaces_created(self):
        var1 = Place()
        sleep(0.05)
        var2 = Place()
        self.assertLess(var1.created_at, var2.created_at)

    def test_2diffplaces_updated(self):
        var1 = Place()
        sleep(0.05)
        var2 = Place()
        self.assertLess(var1.updated_at, var2.updated_at)

    def test_string_rep(self):
        dat = datetime.today()
        dat_repr = repr(dat)
        var = Place()
        var.id = "123456"
        var.created_at = var.updated_at = dat
        varstr = var.__str__()
        self.assertIn("[Place] (123456)", varstr)
        self.assertIn("'id': '123456'", varstr)
        self.assertIn("'created_at': " + dat_repr, varstr)
        self.assertIn("'updated_at': " + dat_repr, varstr)

    def test_ifargs_notused(self):
        var = Place(None)
        self.assertNotIn(None, var.__dict__.values())

    def test_with_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        var = Place(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(var.id, "345")
        self.assertEqual(var.created_at, dat)
        self.assertEqual(var.updated_at, dat)

    def test_without_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
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

    def test_1save(self):
        var = Place()
        sleep(0.05)
        first_updated_at = var.updated_at
        var.save()
        self.assertLess(first_updated_at, var.updated_at)

    def test_2saves(self):
        var = Place()
        sleep(0.05)
        first_updated_at = var.updated_at
        var.save()
        second_updated_at = var.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        var.save()
        self.assertLess(second_updated_at, var.updated_at)

    def test_save_arg(self):
        var = Place()
        with self.assertRaises(TypeError):
            var.save(None)

    def test_save_update(self):
        var = Place()
        var.save()
        plid = "Place." + var.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method."""

    def test_todict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_todict_arg(self):
        var = Place()
        with self.assertRaises(TypeError):
            var.to_dict(None)

    def test_todict_rightkeys(self):
        var = Place()
        self.assertIn("id", var.to_dict())
        self.assertIn("created_at", var.to_dict())
        self.assertIn("updated_at", var.to_dict())
        self.assertIn("__class__", var.to_dict())

    def test_todict_added_attr(self):
        var = Place()
        var.middle_name = "Holberton"
        var.my_number = 98
        self.assertEqual("Holberton", var.middle_name)
        self.assertIn("my_number", var.to_dict())

    def test_todict_datetime_attrib_strings(self):
        var = Place()
        var_dict = var.to_dict()
        self.assertEqual(str, type(var_dict["id"]))
        self.assertEqual(str, type(var_dict["created_at"]))
        self.assertEqual(str, type(var_dict["updated_at"]))

    def test_todict_output(self):
        dat = datetime.today()
        var = Place()
        var.id = "123456"
        var.created_at = var.updated_at = dat
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dat.isoformat(),
            'updated_at': dat.isoformat(),
        }
        self.assertDictEqual(var.to_dict(), tdict)


if __name__ == "__main__":
    unittest.main()
