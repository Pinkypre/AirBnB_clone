#!/usr/bin/python3
"""Unittest module for the BaseModel Class."""

from models import storage
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from datetime import datetime
import json
import os
import re
import time
import unittest
import uuid


class TestBaseModel(unittest.TestCase):

    """Test Cases for the BaseModel class."""

    def setUp(self):
        """Sets up test methods."""
        pass

    def tearDown(self):
        """Tears down test methods."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_3_instantiation(self):
        """Tests instantiation of BaseModel class."""

        b = BaseModel()
        self.assertEqual(str(type(b)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(b, BaseModel)
        self.assertTrue(issubclass(type(b), BaseModel))

    def test_3_init_no_args(self):
        """Tests __init__ with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as output:
            BaseModel.__init__()
        msage = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(output.exception), msage)

    def test_3_init_many_args(self):
        """Tests __init__ with many arguments."""
        self.resetStorage()
        args = [x for x in range(1000)]
        b = BaseModel(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
        b = BaseModel(*args)

    def test_3_attributes(self):
        """Tests attributes value for instance of  BaseModel class."""

        attributes = storage.attributes()["BaseModel"]
        o = BaseModel()
        for k, v in attributes.items():
            self.assertTrue(hasattr(o, k))
            self.assertEqual(type(getattr(o, k, None)), v)

    def test_3_datetime_created(self):
        """Tests if updated_at & created_at are current at creation."""
        date_now = datetime.now()
        b = BaseModel()
        diff = b.updated_at - b.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = b.created_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_3_id(self):
        """Tests  unique user ids."""

        nl = [BaseModel().id for x in range(1000)]
        self.assertEqual(len(set(nl)), len(nl))

    def test_3_save(self):
        """Tests public instance method save()."""

        b = BaseModel()
        time.sleep(0.5)
        date_now = datetime.now()
        b.save()
        diff = b.updated_at - date_now
        self.assertTrue(abs(diff.total_seconds()) < 0.01)

    def test_3_str(self):
        """Tests for __str__ method."""
        b = BaseModel()
        regex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        rex = regex.match(str(b))
        self.assertIsNotNone(rex)
        self.assertEqual(rex.group(1), "BaseModel")
        self.assertEqual(rex.group(2), b.id)
        x = rex.group(3)
        x = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", x)
        l = json.loads(x.replace("'", '"'))
        l2 = b.__dict__.copy()
        l2["created_at"] = repr(l2["created_at"])
        l2["updated_at"] = repr(l2["updated_at"])
        self.assertEqual(l, l2)

    def test_3_to_dict(self):
        """Tests public instance method to_dict()."""

        b = BaseModel()
        b.name = "Aaura"
        b.age = 27
        d = b.to_dict()
        self.assertEqual(d["id"], b.id)
        self.assertEqual(d["__class__"], type(b).__name__)
        self.assertEqual(d["created_at"], b.created_at.isoformat())
        self.assertEqual(d["updated_at"], b.updated_at.isoformat())
        self.assertEqual(d["name"], b.name)
        self.assertEqual(d["age"], b.age)

    def test_3_to_dict_no_args(self):
        """Tests to_dict() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as output:
            BaseModel.to_dict()
        msage = "to_dict() missing 1 required positional argument: 'self'"
        self.assertEqual(str(output.exception), msage)

    def test_3_to_dict_excess_args(self):
        """Tests to_dict() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as output:
            BaseModel.to_dict(self, 98)
        msage = "to_dict() takes 1 positional argument but 2 were given"
        self.assertEqual(str(output.exception), msage)

    def test_4_instantiation(self):
        """Tests instantiation with **kwargs."""

        my_model = BaseModel()
        my_model.name = "Holbert"
        my_model.my_number = 89
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_new_model.to_dict(), my_model.to_dict())

    def test_4_instantiation_dict(self):
        """Tests instantiation with **kwargs from custom dict."""
        d = {"__class__": "BaseModel",
             "updated_at":
             datetime(2050, 12, 30, 23, 59, 59, 123456).isoformat(),
             "created_at": datetime.now().isoformat(),
             "id": uuid.uuid4(),
             "var": "foobar",
             "int": 108,
             "float": 3.14}
        o = BaseModel(**d)
        self.assertEqual(o.to_dict(), d)

    def test_5_save(self):
        """Tests that storage.save() is called from save()."""
        self.resetStorage()
        b = BaseModel()
        b.save()
        key = "{}.{}".format(type(b).__name__, b.id)
        l = {key: b.to_dict()}
        self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path,
                  "r", encoding="utf-8") as Oput:
            self.assertEqual(len(Oput.read()), len(json.dumps(l)))
            Oput.seek(0)
            self.assertEqual(json.load(Oput), l)

    def test_5_save_no_args(self):
        """Tests save() with no arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as output:
            BaseModel.save()
        msage = "save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(output.exception), msage)

    def test_5_save_excess_args(self):
        """Tests save() with too many arguments."""
        self.resetStorage()
        with self.assertRaises(TypeError) as output:
            BaseModel.save(self, 98)
        msage = "save() takes 1 positional argument but 2 were given"
        self.assertEqual(str(output.exception), msage)


if __name__ == '__main__':
    unittest.main()
