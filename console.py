#!/usr/bin/python3
""" Command Interpreter """
import cmd
import sys
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ HBNBCommand class """
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ""

    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    def preloop(self):
        """ Prints if isatty is false """
        if not sys.__stdin__.isatty():
            print("(hbnb)")

    def postcmd(self, stop, line):
        """ Prints if isatty is false """
        if not sys.__stdin__.isatty():
            print("(hbnb) ", end="")
        return stop

    def do_quit(self, arg):
        """ Quit command to exit the program """
        return True

    def do_EOF(self, arg):
        """ EOF command to exit the program """
        print()
        exit()

    def emptyline(self):
        """ An empty line + ENTER shouldn't execute anything """
        pass

    def parse_value(self, value):
        """cast string to float or int if possible"""
        is_valid_value = True
        # To be a valid string it must be of at least length 2 i.e. ""
        # To be a valid string it must begin and end with
        # double quoatation i.e. "sdsds"
        if len(value) >= 2 and value[0] == '"'\
                and value[len(value) - 1] == '"':
            value = value[1:-1]
            value = value.replace("_", " ")
        else:
            try:
                if "." in value:
                    value = float(value)
                else:
                    value = int(value)
            except ValueError:
                is_valid_value = False

        if is_valid_value:
            return value
        else:
            return None
    valid_keys = {
        "BaseModel": ["id", "created_at", "updated_at"],
        "User": [
            "id",
            "created_at",
            "updated_at",
            "email",
            "password",
            "first_name",
            "last_name",
        ],
        "City": ["id", "created_at", "updated_at", "state_id", "name"],
        "State": ["id", "created_at", "updated_at", "name"],
        "Place": [
            "id",
            "created_at",
            "updated_at",
            "city_id",
            "user_id",
            "name",
            "description",
            "number_rooms",
            "number_bathrooms",
            "max_guest",
            "price_by_night",
            "latitude",
            "longitude",
            "amenity_ids"
        ],
        "Amenity": ["id", "created_at", "updated_at", "name"],
        "Review": ["id", "created_at", "updated_at",
                   "place_id", "user_id", "text"],
    }

    def do_create(self, args):
        """Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        args_array = args.split()
        class_name = args_array[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.__classes[class_name]()
        for param_index in range(1, len(args_array)):
            param_array = args_array[param_index].split("=")
            if len(param_array) == 2:
                key = param_array[0]
                if key not in HBNBCommand.valid_keys[class_name]:
                    continue
                value = self.parse_value(param_array[1])
                if value is not None:
                    setattr(new_instance, key, value)
            else:
                pass
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
             Prints the string representation of an instance,
             based on the class name and id.
             Ex: $ show BaseModel 1234-1234-1234.
             Usage: show <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(args[0], args[1])
            if key in objects:
                print(objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
            Deletes an instance based on the class name and id
            (save the change into the JSON file).
            Usage: destroy <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            objects = storage.all()
            key = "{}.{}".format(args[0], args[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                print("** no instance found **")

    def do_all(self, arg):
        """
            Prints all string representation of all instances
            based or not on the class name.
            Usage: all [class name]
        """
        args = arg.split()
        objects = storage.all()
        if not args:
            result = []
            for obj in objects.values():
                result.append(str(obj))
            print(result)
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            class_name = args[0]
            if class_name in HBNBCommand.__classes:
                class_objs = []
                for key, obj in objects.items():
                    if key.startswith(class_name + "."):
                        class_objs.append(str(obj))
                print(class_objs)
            else:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """
            Updates an instance based on the class name and id,
            by adding or updating attribute.
            Usage: update <class name> <id> \
                <attribute name> "<attribute value>"
        """
        objects = storage.all()
        args = shlex.split(arg)

        if len(args) == 0:
            print("** class name missing **")
            return

        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return

        if len(args) == 1:
            print("** instance id missing **")
            return

        key_find = args[0] + '.' + args[1]
        obj = objects.get(key_find, None)

        if not obj:
            print("** no instance found **")
            return

        if len(args) == 2:
            print("** attribute name missing **")
            return

        if len(args) == 3:
            print("** value missing **")
            return

        setattr(obj, args[2], args[3].lstrip('"').rstrip('"'))
        storage.save()

    def default(self, line):
        """
            Method called on input when the command prefix is not recognized.
            In this case it will be used to handle:
                - <class name>.all()
                - <class name>.count()
                - <class name>.show(<id>)
        """
        split_line = line.split(".")
        if len(split_line) != 2:
            print("** invalid command **")

        cls_name = split_line[0]
        meth_arg = split_line[1].split("(")
        if len(meth_arg) != 2:
            print("** invalid command **")

        method = meth_arg[0]
        arg = meth_arg[1].strip(")")
        if method == "all":
            self.do_all(cls_name)
        elif method == "count":
            self.do_count(cls_name)
        elif method == "show":
            self.do_show(cls_name + " " + arg)
        elif method == "destroy":
            self.do_destroy(cls_name + " " + arg)

    def do_count(self, arg):
        """
            Prints numbers of instances based on the class name.
            Usage: <class name>.count()
        """
        class_name = arg
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        objects = storage.all()
        count = 0
        for key in objects.keys():
            if key.startswith(class_name + "."):
                count += 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
