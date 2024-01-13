#!/usr/bin/python3
""" Test """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """ Test """

    def __init__(self, *args, **kwargs):
        """ Test """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ Test """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ Test """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ Test """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ Test """
        new = self.value()
        self.assertEqual(type(new.password), str)
