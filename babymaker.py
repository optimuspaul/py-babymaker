import random
import string
import sys
import uuid

class BabyMaker(object):
    """
    The factory that makes the babies.
    """
    def __init__(self, fields):
        self.fields = fields

    def make_one(self):
        one = dict()
        for name, field in self.fields.iteritems():
            if hasattr(field, "emit"):
                one[name] = field.emit(self)
        return one

    def make_some(self, num):
        for x in range(num):
            yield self.make_one()


class FieldType(object):

    def emit(self, schema):
        return None

class StringType(FieldType):
    """
    Random string of characters.
    """
    def __init__(self, allowed_chars=None, min_size=1, max_size=64):
        self.allowed_chars = allowed_chars or string.printable
        self.max_size = max_size
        self.min_size = min_size

    def emit(self, schema):
        return "".join([random.choice(self.allowed_chars) for x in range(0, random.randint(self.min_size, self.max_size))])


class IntType(FieldType):
    """
    integers, by default it's any positive integer
    """

    def __init__(self, min_value=None, max_value=None):
        self.max_value = max_value or sys.maxint
        self.min_value = min_value or 0

    def emit(self, maker):
        return random.randint(self.min_value, self.max_value)


class EnumType(FieldType):
    """
    For any field that should only be one of a set of choices.
    """
    def __init__(self, choices):
        self.choices = choices

    def emit(self, schema):
        return random.choice(self.choices)



class UUIDType(FieldType):
    """
    Represents a field that should be a UUID
    """
    def __init__(self, format=None):
        self.format = format

    def emit(self, schema):
        if self.format == "int_str":
            return str(uuid.uuid4().int)
        if self.format == "hex_str":
            return uuid.uuid4().hex
        if self.format == "int":
            return uuid.uuid4().int
        return str(uuid.uuid4())


