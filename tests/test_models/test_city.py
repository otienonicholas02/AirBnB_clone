#!/usr/bin/python3
"""Defines unittests for models/city.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_derive(unittest.TestCase):
    """Unittests for testing the city class."""

    def test_forno_args(self):
        self.assertEqual(City, type(City()))

    def test_ifargs_notused(self):
        varcity = City(None)
        self.assertNotIn(None, varcity.__dict__.values())

    def test_fornew_data_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_ifid_public_string(self):
        self.assertEqual(str, type(City().id))

    def test_ifcreated_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_ifupdated_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_ifstateid_public_class_attr(self):
        varcity = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(varcity))
        self.assertNotIn("state_id", varcity.__dict__)

    def test_ifname_public_class_attr(self):
        varcity = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(varcity))
        self.assertNotIn("name", varcity.__dict__)

    def test_2cities_unique_id(self):
        cityx1 = City()
        cityx2 = City()
        self.assertNotEqual(cityx1.id, cityx2.id)

    def test_2cities_diff_created(self):
        cityx1 = City()
        sleep(0.05)
        cityx2 = City()
        self.assertLess(cityx1.created_at, cityx2.created_at)

    def test_2cities_diff_updated(self):
        cityx1 = City()
        sleep(0.05)
        cityx2 = City()
        self.assertLess(cityx1.updated_at, cityx2.updated_at)

    def test_string_rep(self):
        dat = datetime.today()
        dat_repr = repr(dat)
        varcity = City()
        varcity.id = "123456"
        varcity.created_at = varcity.updated_at = dat
        citystr = varcity.__str__()
        self.assertIn("[City] (123456)", citystr)
        self.assertIn("'id': '123456'", citystr)
        self.assertIn("'created_at': " + dat_repr, citystr)
        self.assertIn("'updated_at': " + dat_repr, citystr)

    def test_with_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        varcity = City(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(varcity.id, "345")
        self.assertEqual(varcity.created_at, dat)
        self.assertEqual(varcity.updated_at, dat)

    def test_without_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method."""

    def test_todict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_todict_rightkeys(self):
        cityx = City()
        self.assertIn("id", cityx.to_dict())
        self.assertIn("created_at", cityx.to_dict())
        self.assertIn("updated_at", cityx.to_dict())
        self.assertIn("__class__", cityx.to_dict())

    def test_to_dict_output(self):
        dat = datetime.today()
        cityx = City()
        cityx.id = "123456"
        cityx.created_at = cityx.updated_at = dat
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dat.isoformat(),
            'updated_at': dat.isoformat(),
        }
        self.assertDictEqual(cityx.to_dict(), tdict)

    def test_todict_added_attr(self):
        cityx = City()
        cityx.middle_name = "Holberton"
        cityx.my_number = 98
        self.assertEqual("Holberton", cityx.middle_name)
        self.assertIn("my_number", cityx.to_dict())

    def test_todict_datetime_strings(self):
        cityx = City()
        city_dict = cityx.to_dict()
        self.assertEqual(str, type(city_dict["id"]))
        self.assertEqual(str, type(city_dict["created_at"]))
        self.assertEqual(str, type(city_dict["updated_at"]))

    def test_todict_arg(self):
        cityx = City()
        with self.assertRaises(TypeError):
            cityx.to_dict(None)


class TestCity_save(unittest.TestCase):
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

    def test_save_with_arg(self):
        cityx = City()
        with self.assertRaises(TypeError):
            cityx.save(None)

    def test_save_updates_file(self):
        cityx = City()
        cityx.save()
        cityid = "City." + cityx.id
        with open("file.json", "r") as f:
            self.assertIn(cityid, f.read())

    def test_one_save(self):
        cityx = City()
        sleep(0.05)
        first_updated_at = cityx.updated_at
        cityx.save()
        self.assertLess(first_updated_at, cityx.updated_at)

    def test_two_saves(self):
        cityx = City()
        sleep(0.05)
        first_updated_at = cityx.updated_at
        cityx.save()
        second_updated_at = cityx.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cityx.save()
        self.assertLess(second_updated_at, cityx.updated_at)


if __name__ == "__main__":
    unittest.main()
