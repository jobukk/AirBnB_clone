#!/usr/bin/python3
"""Testcase for Basemodel class"""
import unittest
from models.base_model import BaseModel
from datetime import datetime
import uuid


class TestBaseModel(unittest.TestCase):
    """Unittestcase for class basemodel"""
    def setUp(self):
        self.model = BaseModel()

    def tearDown(self):
        del self.model

    def test_init(self):
        self.assertIsNotNone(self.model.id)
        self.assertIsInstance(self.model.created_at, datetime)
        self.assertIsInstance(self.model.updated_at, datetime)

    def test_str(self):
        self.assertEqual(
            str(self.model),
            f"[BaseModel] ({self.model.id}) {self.model.__dict__}"
        )

    def test_to_dict(self):
        self.model.name = "My_First_Model"
        self.model.my_number = 89
        model_dict = self.model.to_dict()
        expected_keys = [
            'id',
            'created_at',
            'updated_at',
            'name',
            'my_number',
            '__class__'
        ]
        self.assertCountEqual(model_dict.keys(), expected_keys)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        self.assertEqual(model_dict['name'], 'My_First_Model')
        self.assertEqual(model_dict['my_number'], 89)

    def test_new_instance_from_dict(self):
        self.model.name = "My_First_Model"
        self.model.my_number = 89
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertEqual(self.model.id, new_model.id)
        self.assertEqual(self.model.created_at, new_model.created_at)
        self.assertEqual(self.model.updated_at, new_model.updated_at)
        self.assertEqual(self.model.name, new_model.name)
        self.assertEqual(self.model.my_number, new_model.my_number)


if __name__ == '__main__':
    unittest.main()
