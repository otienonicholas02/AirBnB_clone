#!/usr/bin/python3
"""Defines unittests for the state.py."""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_derive(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_ifno_args(self):
        self.assertEqual(State, type(State()))

    def test_ifargs_notused(self):
        statex = State(None)
        self.assertNotIn(None, statex.__dict__.values())

    def test_with_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        statex = State(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(statex.id, "345")
        self.assertEqual(statex.created_at, dat)
        self.assertEqual(statex.updated_at, dat)

    def test_without_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_ifnew_data_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_ifid_public_string(self):
        self.assertEqual(str, type(State().id))

    def test_ifcreated_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_ifupdated_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_ifname_public_class_attr(self):
        statex = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(statex))
        self.assertNotIn("name", statex.__dict__)

    def test_2states_unique(self):
        statex1 = State()
        statex2 = State()
        self.assertNotEqual(statex1.id, statex2.id)

    def test_2states_diff_created(self):
        statex1 = State()
        sleep(0.05)
        statex2 = State()
        self.assertLess(statex1.created_at, statex2.created_at)

    def test_2states_diff_updated(self):
        statex1 = State()
        sleep(0.05)
        statex2 = State()
        self.assertLess(statex1.updated_at, statex2.updated_at)

    def test_string_rep(self):
        dat = datetime.today()
        dat_repr = repr(dat)
        statex = State()
        statex.id = "123456"
        statex.created_at = statex.updated_at = dat
        ststr = statex.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dat_repr, ststr)
        self.assertIn("'updated_at': " + dat_repr, ststr)


class TestState_save(unittest.TestCase):
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
        statex = State()
        sleep(0.05)
        first_updated_at = statex.updated_at
        statex.save()
        self.assertLess(first_updated_at, statex.updated_at)

    def test_2saves(self):
        statex = State()
        sleep(0.05)
        first_updated_at = statex.updated_at
        statex.save()
        second_updated_at = statex.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        statex.save()
        self.assertLess(second_updated_at, statex.updated_at)

    def test_save_arg(self):
        statex = State()
        with self.assertRaises(TypeError):
            statex.save(None)

    def test_save_updates(self):
        statex = State()
        statex.save()
        stid = "State." + statex.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing the to_dict method."""

    def test_todict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_todict_rightkeys(self):
        statex = State()
        self.assertIn("id", statex.to_dict())
        self.assertIn("created_at", statex.to_dict())
        self.assertIn("updated_at", statex.to_dict())
        self.assertIn("__class__", statex.to_dict())

    def test_todict_with_arg(self):
        statex = State()
        with self.assertRaises(TypeError):
            statex.to_dict(None)

    def test_todict_added_attr(self):
        statex = State()
        statex.middle_name = "Holberton"
        statex.my_number = 98
        self.assertEqual("Holberton", statex.middle_name)
        self.assertIn("my_number", statex.to_dict())

    def test_todict_datetime_attr_strings(self):
        statex = State()
        st_dict = statex.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_todict_output(self):
        dat = datetime.today()
        statex = State()
        statex.id = "123456"
        statex.created_at = statex.updated_at = dat
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dat.isoformat(),
            'updated_at': dat.isoformat(),
        }
        self.assertDictEqual(statex.to_dict(), tdict)


if __name__ == "__main__":
    unittest.main()
