#!/usr/bin/python3
"""Entry point of the command interpreter."""

import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):

    """Class for the command interpreter."""

    prompt = "(hbnb) "

    def emptyline(self):
        """Does nothing upon receieving an empty line.
        """
        pass

    def default(self, line):
        """Catch commands if nothing else matches then."""
        # print("DEF:::", line)
        self._precmd(line)

    def do_EOF(self, line):
        """EOF signal to exit the program.
        """
        print()
        return True

    def do_quit(self, line):
        """Exits the program.
        """
        return True

    def do_create(self, line):
        """Creates an instance.
        """
        if line == "" or line is None:
            print("** class name missing **")
        elif line not in storage.classes():
            print("** class doesn't exist **")
        else:
            b = storage.classes()[line]()
            b.save()
            print(b.id)

    def do_show(self, line):
        """Display the string representation of an instance.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            cmand = line.split(' ')
            if cmand[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(cmand) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(cmand[0], cmand[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, line):
        """Deletes a class instance of a given id.
        """
        if line == "" or line is None:
            print("** class name missing **")
        else:
            cmand = line.split(' ')
            if cmand[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(cmand) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(cmand[0], cmand[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, line):
        """Display all string representation of all instances.
        """
        if line != "":
            cmand = line.split(' ')
            if cmand[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                ncl = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == cmand[0]]
                print(ncl)
        else:
            new_list = [str(obj) for key, obj in storage.all().items()]
            print(new_list)

    def do_update(self, line):
        """ Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        """
        if line == "" or line is None:
            print("** class name missing **")
            return

        regex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(regex, line)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                dump = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        dump = float
                    else:
                        dump = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif dump:
                    try:
                        value = dump(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_count(self, line):
        """Counts the instances of a class.
        """
        cmand = line.split(' ')
        if not cmand[0]:
            print("** class name missing **")
        elif cmand[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            ties = [
                k for k in storage.all() if k.startswith(
                    cmand[0] + '.')]
            print(len(ties))

if __name__ == '__main__':
    HBNBCommand().cmdloop()
