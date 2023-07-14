#!/usr/bin/python3
"""Defines unittests for the review class"""


import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_derive(unittest.TestCase):
    """Unittests for testing the Review class."""

    def test_forno_args(self):
        self.assertEqual(Review, type(Review()))

    def test_new_data_in_object(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_2reviews_unique(self):
        rev1 = Review()
        rev2 = Review()
        self.assertNotEqual(rev1.id, rev2.id)

    def test_2reviews_diff_created(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.created_at, rev2.created_at)

    def test_ifid_public_string(self):
        self.assertEqual(str, type(Review().id))

    def test_ifcreated_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_ifupdated_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_ifplace_public_class_attr(self):
        rev = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rev))
        self.assertNotIn("place_id", rev.__dict__)

    def test_ifuser_id_public_class_attr(self):
        rev = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rev))
        self.assertNotIn("user_id", rev.__dict__)

    def test_words_public_class_attr(self):
        rev = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rev))
        self.assertNotIn("text", rev.__dict__)

    def test_2reviews_diff_updated(self):
        rev1 = Review()
        sleep(0.05)
        rev2 = Review()
        self.assertLess(rev1.updated_at, rev2.updated_at)

    def test_string_rep(self):
        dat = datetime.today()
        dat_repr = repr(dat)
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = dat
        rvstr = rev.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dat_repr, rvstr)
        self.assertIn("'updated_at': " + dat_repr, rvstr)

    def test_ifargs_notused(self):
        rev = Review(None)
        self.assertNotIn(None, rev.__dict__.values())

    def test_with_kwargs(self):
        dat = datetime.today()
        dat_iso = dat.isoformat()
        rev = Review(id="345", created_at=dat_iso, updated_at=dat_iso)
        self.assertEqual(rev.id, "345")
        self.assertEqual(rev.created_at, dat)
        self.assertEqual(rev.updated_at, dat)

    def test_without_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing the save method."""

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
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        self.assertLess(first_updated_at, rev.updated_at)

    def test_2saves(self):
        rev = Review()
        sleep(0.05)
        first_updated_at = rev.updated_at
        rev.save()
        second_updated_at = rev.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rev.save()
        self.assertLess(second_updated_at, rev.updated_at)

    def test_save_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.save(None)

    def test_save_updates(self):
        rev = Review()
        rev.save()
        rvid = "Review." + rev.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing the to_dict method."""

    def test_todict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_todict_arg(self):
        rev = Review()
        with self.assertRaises(TypeError):
            rev.to_dict(None)

    def test_todict_rightkeys(self):
        rev = Review()
        self.assertIn("id", rev.to_dict())
        self.assertIn("created_at", rev.to_dict())
        self.assertIn("updated_at", rev.to_dict())
        self.assertIn("__class__", rev.to_dict())

    def test_todict_added_attr(self):
        rev = Review()
        rev.middle_name = "Holberton"
        rev.my_number = 98
        self.assertEqual("Holberton", rev.middle_name)
        self.assertIn("my_number", rev.to_dict())
        
    def test_todict_output(self):
        dat = datetime.today()
        rev = Review()
        rev.id = "123456"
        rev.created_at = rev.updated_at = dat
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dat.isoformat(),
            'updated_at': dat.isoformat(),
        }
        self.assertDictEqual(rev.to_dict(), tdict)


if __name__ == "__main__":
    unittest.main()
