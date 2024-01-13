#!/usr/bin/python3
"""document document"""

from models.engine.db_storage import DBStorage
import os
import unittest


@unittest.skipIf(
    os.getenv("HBNB_TYPE_STORAGE") != "db",
    "Test is not relevant for DBStorage"
)
class test_DB_Storage(unittest.TestCase):
    """document document"""

    def setUp(self):
        self.storage = DBStorage()

    def test_documentation(self):
        """document document"""
        self.assertIsNot(DBStorage.__doc__, None)

    def test_get(self):
        """ Add an object to storage File """
        obj = DBStorage()
        self.storage.new(obj)
        self.storage.save()

        # Test that the correct object is returned
        self.assertEqual(self.storage.get(DBStorage, obj.id), obj)

        # Test that None is returned if No object found
        self.assertEqual(self.storage.get(
            DBStorage, "No object found with this ID"))

    def test_count(self):
        """ Add some objects to storage """
        for obj in range(5):
            obj = DBStorage()
            self.storage.new(obj)
        self.storage.save()

        # Test that the correct count is returned
        self.assertEqual(self.storage.count(DBStorage), 5)

        # Test that the count of all object is returned if No class passed
        self.assertEqual(self.storage.count(), 5)
