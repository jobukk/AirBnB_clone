#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from models.base_model import BaseModel
from models import storage
from datetime import datetime
from shlex import shlex
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """This is command prompt to control Airbnb clone functionality"""

    prompt = "(hbnb) "
    __classes = {
            'BaseModel': BaseModel,
            'User': User,
            'State': State,
            'City': City,
            'Amenity': Amenity,
            'Place': Place,
            'Review': Review,
    }

    def emptyline(self):
        """do nothing"""
        pass

    def do_EOF(self, line):
        """EOF"""
        print("")
        return True

    # def help_EOF(self):
    #     """help EOF"""
    #     print("EOF  help  quit")

    def do_quit(self, line):
        """quit command"""
        return True

    def help_quit(self):
        """help quit"""
        print("Quit command to exit the program")
        print()

    def do_create(self, line):
        """$ create BaseModel"""
        arg = line.split()
        if len(arg) == 0:
            print("** class name missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg[0])().id)
            storage.save()

    def do_show(self, line):
        """display data in a dictionary"""
        arg = line.split()
        obj = storage.all()
        print(arg)
        if len(arg) == 0:
            print("** class name missing **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj:
            print("** no instance found **")
        else:
            print(obj["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, line):
        """$ destroy BaseModel 1234-1234-1234"""
        arg = line.split()
        obj = storage.all()
        print(arg)
        if len(arg) == 0:
            print("** class name missing **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif "{}.{}".format(arg[0], arg[1]) not in obj:
            print("** no instance found **")
        else:
            del obj["{}.{}".format(arg[0], arg[1])]
        storage.save()

    def do_all(self, line):
        """$ all"""
        arg = line.split()
        obj = storage.all()
        if arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        else:
            objl = []
            for k, v in obj.items():
                if type(v) is self.__classes.get(arg[0]):
                    objl.append(str(v))
            print(objl)

    def do_update(self, line):
        """update <class name> <id> <attribute name> "<attribute value>"""
        arg = line.split()
        obj = storage.all()
        clsname, objid, attrname, attrval = None, None, None, None
        if len(arg) > 0:
            clsname = arg[0]
        if len(arg) > 1:
            objid = arg[1]
        if len(arg) > 2:
            attrname = arg[2]
        if len(arg) > 3:
            attrval = ' '.join(arg[3:]).strip('"')

        if len(arg) == 0:
            print("** class name missing **")
            return False
        if arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg[0], arg[1]) not in obj.keys():
            print("** no instance found **")
            return False
        if len(arg) == 2:
            print("** attribute name missing **")
            return False
        if len(arg) == 3:
            print('** value missing **')
            return False
        obj_key = "{}.{}".format(clsname, objid)
        obj = obj.get(obj_key)
        if obj is None:
            print("** no instance found **")
            return False
        print(obj)
        setattr(obj, attrname, attrval)
        print("Attribute updated successfully")
        print(obj)
        storage.save()

    def default(self, line):
        """handle class commands"""
        ln = line.split('.', 1)
        if len(ln) < 2:
            print('*** Unknown syntax:', ln[0])
            return False
        clsname, line = ln[0], ln[1]
        if clsname not in list(self.__classes.keys()):
            print('*** Unknown syntax: {}.{}'.format(clsname, line))
            return False
        ln = line.split('(', 1)
        if len(ln) < 2:
            print('*** Unknown syntax: {}.{}'.format(clsname, ln[0]))
            return False
        mthname, args = ln[0], ln[1].rstrip(')')
        if mthname not in ['all', 'count', 'show', 'destroy', 'update']:
            print('*** Unknown syntax: {}.{}'.format(clsname, line))
            return False
        if mthname == 'all':
            self.do_all(clsname)
        elif mthname == 'count':
            print(self.count_class(clsname))
        elif mthname == 'show':
            self.do_show(clsname + " " + args.strip('"'))
        elif mthname == 'destroy':
            self.do_destroy(clsname + " " + args.strip('"'))
        elif mthname == 'update':
            lb, rb = args.find('{'), args.find('}')
            d = None
            if args[lb:rb + 1] != '':
                d = eval(args[lb:rb + 1])
            ln = args.split(',', 1)
            objid, args = ln[0].strip('"'), ln[1]
            if d and type(d) is dict:
                self.handle_dict(clsname, objid, d)
            else:
                from shlex import shlex
                args = args.replace(',', ' ', 1)
                ln = list(shlex(args))
                ln[0] = ln[0].strip('"')
                self.do_update(" ".join([clsname, objid, ln[0], ln[1]]))

    def handle_dict(self, clsname, objid, d):
        """handle dictionary update"""
        for k, v in d.items():
            self.do_update(" ".join([clsname, objid, str(k), str(v)])) 

    @staticmethod
    def count_class(clsname):
        """count number of objects of type clsname"""
        c = 0
        for k, v in storage.all().items():
            if type(v).__name__ == clsname:
                c += 1
        return (c)           


if __name__ == '__main__':
    HBNBCommand().cmdloop()
