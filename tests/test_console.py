#!/usr/bin/python3
"""Defines unittests for console.py"""

from console import HBNBCommand
from models.engine.file_storage import FileStorage
import unittest
import datetime
from unittest.mock import patch
import sys
from io import StringIO
import re
import os


class TestHBNBCommand(unittest.TestCase):

    """Tests HBNBCommand console."""

    attribute_values = {
        str: "foobar108",
        int: 1008,
        float: 1.08
    }

    reset_values = {
        str: "",
        int: 0,
        float: 0.0
    }

    test_random_attributes = {
        "strfoo": "barfoo",
        "intfoo": 248,
        "floatfoo": 9.8
    }

    def setUp(self):
        """Sets up test cases."""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        self.resetStorage()

    def resetStorage(self):
        """Resets FileStorage data."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_help(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help")
        x = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(x, Oput.getvalue())

    def test_help_EOF(self):
        """Tests  help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help EOF")
        x = 'Handles End Of File character.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_help_quit(self):
        """Tests  help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help quit")
        x = 'Exits the program.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_help_create(self):
        """Tests  help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help create")
        x = 'Creates an instance.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_help_show(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help show")
        x = 'Prints string representation of an instance.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_help_destroy(self):
        """Tests  help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help destroy")
        x = 'Deletes an instance based on the class name and id.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_help_all(self):
        """Tests help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help all")
        x = 'Prints all string representation of all instances.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_help_count(self):
        """Tests help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help count")
        x = 'Counts instances of a class.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_help_update(self):
        """Tests help command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("help update")
        x = 'Updates an instance by adding or updating attribute.\n        \n'
        self.assertEqual(x, Oput.getvalue())

    def test_do_quit(self):
        """Tests quit commmand."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("quit")
        msage = Oput.getvalue()
        self.assertTrue(len(msage) == 0)
        self.assertEqual("", msage)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("quit garbage")
        msage = Oput.getvalue()
        self.assertTrue(len(msage) == 0)
        self.assertEqual("", msage)

    def test_do_EOF(self):
        """Tests EOF commmand."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("EOF")
        msage = Oput.getvalue()
        self.assertTrue(len(msage) == 1)
        self.assertEqual("\n", msage)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("EOF garbage")
        msage = Oput.getvalue()
        self.assertTrue(len(msage) == 1)
        self.assertEqual("\n", msage)

    def test_emptyline(self):
        """Tests emptyline."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("\n")
        x = ""
        self.assertEqual(x, Oput.getvalue())

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("                  \n")
        x = ""
        self.assertEqual(x, Oput.getvalue())

    def test_do_create(self):
        """Tests create for all classes."""
        for classname in self.classes():
            self.help_test_do_create(classname)

    def help_test_do_create(self, classname):
        """Helps method to test the create commmand."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = Oput.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "{}.{}".format(classname, uid)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("all {}".format(classname))
        self.assertTrue(uid in Oput.getvalue())

    def test_do_create_error(self):
        """Tests create command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create garbage")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

    def test_do_show(self):
        """Tests show for all classes."""
        for classname in self.classes():
            self.help_test_do_show(classname)
            self.help_test_show_advanced(classname)

    def help_test_do_show(self, classname):
        """Helps test the show command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = Oput.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("show {} {}".format(classname, uid))
        x = Oput.getvalue()[:-1]
        self.assertTrue(uid in x)

    def test_do_show_error(self):
        """Tests show command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("show")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("show garbage")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("show BaseModel")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("show BaseModel 121212")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** no instance found **")

    def help_test_show_advanced(self, classname):
        """Helps test .show() command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = Oput.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertTrue(uid in x)

    def test_do_show_error_advanced(self):
        """Tests show() command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(".show()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("garbage.show()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("BaseModel.show()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('BaseModel.show("121212")')
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** no instance found **")

    def test_do_destroy(self):
        """Tests destroy for all classes."""
        for classname in self.classes():
            self.help_test_do_destroy(classname)
            self.help_test_destroy_advanced(classname)

    def help_test_do_destroy(self, classname):
        """Helps test destroy command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = Oput.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("destroy {} {}".format(classname, uid))
        x = Oput.getvalue()[:-1]
        self.assertTrue(len(x) == 0)

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in Oput.getvalue())

    def test_do_destroy_error(self):
        """Tests destroy command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("destroy")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("destroy garbage")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("destroy BaseModel")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("destroy BaseModel 121212")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** no instance found **")

    def help_test_destroy_advanced(self, classname):
        """Helps test destroy command."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = Oput.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.destroy("{}")'.format(classname, uid))
        x = Oput.getvalue()[:-1]
        self.assertTrue(len(x) == 0)

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in Oput.getvalue())

    def test_do_destroy_error_advanced(self):
        """Tests destroy() command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(".destroy()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("garbage.destroy()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("BaseModel.destroy()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('BaseModel.destroy("121212")')
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** no instance found **")

    def test_do_all(self):
        """Tests all for all classes."""
        for classname in self.classes():
            self.help_test_do_all(classname)
            self.help_test_all_advanced(classname)

    def help_test_do_all(self, classname):
        """Helps test all command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("all")
        x = Oput.getvalue()[:-1]
        self.assertTrue(len(x) > 0)
        self.assertIn(uid, x)

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("all {}".format(classname))
        x = Oput.getvalue()[:-1]
        self.assertTrue(len(x) > 0)
        self.assertIn(uid, x)

    def test_do_all_error(self):
        """Tests all command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("all garbage")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

    def help_test_all_advanced(self, classname):
        """Helps test the .all() command."""
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("{}.all()".format(classname))
        x = Oput.getvalue()[:-1]
        self.assertTrue(len(x) > 0)
        self.assertIn(uid, x)

    def test_do_all_error_advanced(self):
        """Tests all() command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("garbage.all()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

    def test_count_all(self):
        """Tests count for all classes."""
        for classname in self.classes():
            self.help_test_count_advanced(classname)

    def help_test_count_advanced(self, classname):
        """Helps test .count() command."""
        for i in range(20):
            uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("{}.count()".format(classname))
        x = Oput.getvalue()[:-1]
        self.assertTrue(len(x) > 0)
        self.assertEqual(x, "20")

    def test_do_count_error(self):
        """Tests .count() command with errors."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("garbage.count()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(".count()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

    def test_update_1(self):
        """Tests update 1..."""
        classname = "BaseModel"
        atribut = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        x = Oput.getvalue()
        self.assertEqual(len(x), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(atribut, x)
        self.assertIn(val, x)

    def test_update_2(self):
        """Tests update 1..."""
        classname = "User"
        atribut = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        x = Oput.getvalue()
        self.assertEqual(len(x), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(atribut, x)
        self.assertIn(val, x)

    def test_update_3(self):
        """Tests update 1..."""
        classname = "City"
        atribut = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        x = Oput.getvalue()
        self.assertEqual(len(x), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(atribut, x)
        self.assertIn(val, x)

    def test_update_4(self):
        """Tests update 1..."""
        classname = "State"
        atribut = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        x = Oput.getvalue()
        self.assertEqual(len(x), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(atribut, x)
        self.assertIn(val, x)

    def test_update_5(self):
        """Tests update 1..."""
        classname = "Amenity"
        atribut = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        x = Oput.getvalue()
        self.assertEqual(len(), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(atribut, x)
        self.assertIn(val, x)

    def test_update_6(self):
        """Tests update 1..."""
        classname = "Review"
        atribut = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        x = Oput.getvalue()
        self.assertEqual(len(x), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(atribut, x)
        self.assertIn(val, x)

    def test_update_7(self):
        """Tests update 1..."""
        classname = "Place"
        atribut = "foostr"
        val = "fooval"
        uid = self.create_class(classname)
        cmd = '{}.update("{}", "{}", "{}")'
        #  cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, val)
        #  print("CMD::", cmd)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        x = Oput.getvalue()
        self.assertEqual(len(x), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(atribut, x)
        self.assertIn(val, x)

    def test_update_everything(self):
        """Tests update command with errthang, like a baws."""
        for classname, cls in self.classes().items():
            uid = self.create_class(classname)
            for atribut, value in self.test_random_attributes.items():
                if type(value) is not str:
                    pass
                quotes = (type(value) == str)
                self.help_test_update(classname, uid, atribut,
                                      value, quotes, False)
                self.help_test_update(classname, uid, atribut,
                                      value, quotes, True)
            pass
            if classname == "BaseModel":
                continue
            for atribut, atribut_type in self.attributes()[classname].items():
                if atribut_type not in (str, int, float):
                    continue
                self.help_test_update(classname, uid, atribut,
                                      self.attribute_values[atribut_type],
                                      True, False)
                self.help_test_update(classname, uid, atribut,
                                      self.attribute_values[atribut_type],
                                      False, True)

    def help_test_update(self, classname, uid, atribut, val, quotes, func):
        """Tests update commmand."""
        #  print("QUOTES", quotes)
        FileStorage._FileStorage__objects = {}
        if os.path.isfile("file.json"):
            os.remove("file.json")
        uid = self.create_class(classname)
        value_str = ('"{}"' if quotes else '{}').format(val)
        if func:
            cmd = '{}.update("{}", "{}", {})'
        else:
            cmd = 'update {} {} {} {}'
        cmd = cmd.format(classname, uid, atribut, value_str)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(cmd)
        msage = Oput.getvalue()[:-1]
        # print("MSG::", msg)
        # print("CMD::", cmd)
        self.assertEqual(len(msage), 0)
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        x = Oput.getvalue()
        self.assertIn(str(val), x)
        self.assertIn(attr, x)

    def test_do_update_error(self):
        """Tests update command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("update")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("update garbage")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("update BaseModel")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("update BaseModel 121212")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('update BaseModel {}'.format(uid))
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('update BaseModel {} name'.format(uid))
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** value missing **")

    def test_do_update_error_advanced(self):
        """Tests update() command with errors."""
        uid = self.create_class("BaseModel")
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd(".update()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("garbage.update()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("BaseModel.update()")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("BaseModel.update(121212)")
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('BaseModel.update("{}")'.format(uid))
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd('BaseModel.update("{}", "name")'.format(uid))
        msage = Oput.getvalue()[:-1]
        self.assertEqual(msage, "** value missing **")

    def create_class(self, classname):
        """Creates a class for console tests."""
        with patch('sys.stdout', new=StringIO()) as Oput:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = Oput.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        return uid

    def help_load_dict(self, rep):
        """Helper method to test dictionary equality."""
        regex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        rex = regex.match(rep)
        self.assertIsNotNone(rex)
        x = rex.group(3)
        x = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        l = json.loads(x.replace("'", '"'))
        return l

    def classes(self):
        """Returns a dictionary of valid classes and their references."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def attributes(self):
        """Returns the valid attributes and their types for classname."""
        attributes = {
            "BaseModel":
                     {"id": str,
                      "created_at": datetime.datetime,
                      "updated_at": datetime.datetime},
            "User":
                     {"email": str,
                      "password": str,
                      "first_name": str,
                      "last_name": str},
            "State":
                     {"name": str},
            "City":
                     {"state_id": str,
                      "name": str},
            "Amenity":
                     {"name": str},
            "Place":
                     {"city_id": str,
                      "user_id": str,
                      "name": str,
                      "description": str,
                      "number_rooms": int,
                      "number_bathrooms": int,
                      "max_guest": int,
                      "price_by_night": int,
                      "latitude": float,
                      "longitude": float,
                      "amenity_ids": list},
            "Review":
                     {"place_id": str,
                      "user_id": str,
                      "text": str}
        }
        return attributes


if __name__ == "__main__":
    unittest.main()
