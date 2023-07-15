#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
from shlex import split




class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """No action taken when receiving and empty line."""
        pass

    def default(self, arg):
        """Default for the module when an invalid input is entered."""
        argumendict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argumendict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argumendict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_create(self, arg):
        """Create a new class instance and print its id."""
        argvar = parse(arg)
        if len(argvar) == 0:
            print("** class name missing **")
        elif argvar[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argvar[0])().id)
            storage.save()

    def do_quit(self, arg):
        """Function for the quit commmand to exit the program."""
        return True

    def do_EOF(self, arg):
        """Command EOF to exit the program."""
        print("")
        return True

    def do_show(self, arg):
        """Show the string representation of a given id."""
        argx = parse(arg)
        objdict = storage.all()
        if len(argx) == 0:
            print("** class name missing **")
        elif argx[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argx) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argx[0], argx[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argx[0], argx[1])])

    def do_destroy(self, arg):
        """Function to delete a class instance of a given id."""
        argvar = parse(arg)
        objdict = storage.all()
        if len(argvar) == 0:
            print("** class name missing **")
        elif argvar[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argvar) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argvar[0], argvar[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argvar[0], argvar[1])]
            storage.save()

    def do_all(self, arg):
        """Shows a string representations of all instances of a given class."""
        argx = parse(arg)
        if len(argx) > 0 and argx[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argx) > 0 and argx[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argx) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Count the number of instances of a given class."""
        argx = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argx[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Update a class instance of a given id."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


def parse(arg):
    curly_brackets = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_brackets is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_brackets.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_brackets.group())
        return retl

if __name__ == "__main__":
    HBNBCommand().cmdloop()
