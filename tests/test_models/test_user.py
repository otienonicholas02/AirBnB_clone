#!/usr/bin/python3
"""Defines unittests for user.py."""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_derive(unittest.TestCase):
    """Unittests for testing the User class."""

    def test_ifno_args(self):
        self.assertEqual(User, type(User()))

    def test_with_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        use = User(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(use.id, "345")
        self.assertEqual(use.created_at, dat)
        self.assertEqual(use.updated_at, dat)

    def test_without_kwargs(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_ifnew_data_in_objects(self):
        self.assertIn(User(), models.storage.all().values())

    def test_ifid_public_string(self):
        self.assertEqual(str, type(User().id))

    def test_ifcreated_public_datetime(self):
        self.assertEqual(datetime, type(User().created_at))

    def test_ifupdated_public_datetime(self):
        self.assertEqual(datetime, type(User().updated_at))

    def test_ifemail_public_string(self):
        self.assertEqual(str, type(User.email))

    def test_ifpassword_public_string(self):
        self.assertEqual(str, type(User.password))

    def test_first_name_public_string(self):
        self.assertEqual(str, type(User.first_name))

    def test_last_name_public_string(self):
        self.assertEqual(str, type(User.last_name))

    def test_2users_unique(self):
        use1 = User()
        use2 = User()
        self.assertNotEqual(use1.id, use2.id)

    def test_2users_diff_created(self):
        use1 = User()
        sleep(0.05)
        use2 = User()
        self.assertLess(use1.created_at, use2.created_at)

    def test_2users_diff_updated(self):
        use1 = User()
        sleep(0.05)
        use2 = User()
        self.assertLess(use1.updated_at, use2.updated_at)

    def test_string_rep(self):
        dat = datetime.today()
        dat_repr = repr(dat)
        use = User()
        use.id = "123456"
        use.created_at = use.updated_at = dat
        usstr = use.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dat_repr, usstr)
        self.assertIn("'updated_at': " + dat_repr, usstr)

    def test_ifargs_notused(self):
        use = User(None)
        self.assertNotIn(None, use.__dict__.values()) 


class TestUser_save(unittest.TestCase):
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

    def test_save_arg(self):
        use = User()
        with self.assertRaises(TypeError):
            use.save(None)
    
    def test_1save(self):
        use = User()
        sleep(0.05)
        first_updated_at = use.updated_at
        use.save()
        self.assertLess(first_updated_at, use.updated_at)

    def test_2saves(self):
        use = User()
        sleep(0.05)
        first_updated_at = use.updated_at
        use.save()
        second_updated_at = use.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        use.save()
        self.assertLess(second_updated_at, use.updated_at)

    def test_save_updates(self):
        use = User()
        use.save()
        usid = "User." + use.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for testing the to_dict method."""

    def test_todict_type(self):
        self.assertTrue(dict, type(User().to_dict()))

    def test_todict_rightkeys(self):
        use = User()
        self.assertIn("id", use.to_dict())
        self.assertIn("created_at", use.to_dict())
        self.assertIn("updated_at", use.to_dict())
        self.assertIn("__class__", use.to_dict())

    def test_todict_arg(self):
        use = User()
        with self.assertRaises(TypeError):
            use.to_dict(None)

    def test_todict_added_attr(self):
        use = User()
        use.middle_name = "Holberton"
        use.my_number = 98
        self.assertEqual("Holberton", use.middle_name)
        self.assertIn("my_number", use.to_dict())

    def test_todict_datetime_strings(self):
        use = User()
        use_dict = use.to_dict()
        self.assertEqual(str, type(use_dict["id"]))
        self.assertEqual(str, type(use_dict["created_at"]))
        self.assertEqual(str, type(use_dict["updated_at"]))

    def test_todict_output(self):
        dat = datetime.today()
        use = User()
        use.id = "123456"
        use.created_at = use.updated_at = dat
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dat.isoformat(),
            'updated_at': dat.isoformat(),
        }
        self.assertDictEqual(use.to_dict(), tdict)


if __name__ == "__main__":
    unittest.main()
