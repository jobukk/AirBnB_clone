#!/usr/bin/python3
"""Defines test of Filestorage"""
import unittest
import os
import json
from unittest.mock import patch
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from file_storage import FileStorage  # Assuming your FileStorage class is in a file named 'file_storage.py'


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.storage = FileStorage()

    def tearDown(self):
        if os.path.exists(self.storage._FileStorage__file_path):
            os.remove(self.storage._FileStorage__file_path)

    def test_all(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        obj = BaseModel()
        self.storage.new(obj)
        self.assertIn('BaseModel.{}'.format(obj.id), self.storage.all())

    def test_save_reload(self):
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.storage.new(obj1)
        self.storage.new(obj2)
        self.storage.save()

        new_storage = FileStorage()
        new_storage.reload()

        self.assertIn('BaseModel.{}'.format(obj1.id), new_storage.all())
        self.assertIn('BaseModel.{}'.format(obj2.id), new_storage.all())

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save(self, mock_open):
        obj = BaseModel()
        self.storage.new(obj)
        self.storage.save()
        mock_open.assert_called_once_with(self.storage._FileStorage__file_path, 'w')

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_reload(self, mock_open):
        data = {'BaseModel.1': {'id': '1', 'name': 'Test'}}
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(data)
        self.storage.reload()
        self.assertIn('BaseModel.1', self.storage.all())


if __name__ == '__main__':
    unittest.main()
