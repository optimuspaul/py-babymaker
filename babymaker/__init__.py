import random
import string
import sys
import uuid
from datetime import datetime, timedelta


class BabyMaker(object):
    """
    The factory that makes the babies.
    """
    def __init__(self, fields):
        self.fields = fields
        self.last_iteration = None
        self.current_iteration = None

    def make_one(self):
        """
        TODO - allow a field to raise an exception that it requires another field before it
            can be processed, which would retry the field after all other fields are done.
            Will need to be careful of circular dependencies.
        """
        self.last_iteration = self.current_iteration
        self.current_iteration = dict()
        for name, field in self.fields.items():
            if hasattr(field, "emit"):
                self.current_iteration[name] = field.emit(self)
        return DictObject(self.current_iteration)

    def make_some(self, num):
        for x in range(num):
            yield self.make_one()


class DictObject(dict):
    """
    A dict implementation that provides several extra conveniences.
    """
    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        if type(value) is dict:
            value = DictObject(value)
            self[key] = value
        return value

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value


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
        self.max_value = max_value or sys.maxsize
        self.min_value = min_value or 0

    def emit(self, maker):
        return random.randint(self.min_value, self.max_value)


class FloatType(FieldType):
    """
    floats, default random from 0.0 to 1.0
    if max_value <= min_value then max_value = min_value * 2.0
    """

    def __init__(self, min_value=None, max_value=None):
        self.max_value = max_value or 1.0
        self.min_value = min_value or 0.0
        if self.max_value <= self.min_value:
            self.max_value = self.min_value * 2.0

    def emit(self, schema):
        return random.uniform(self.min_value, self.max_value)


class EnumType(FieldType):
    """
    For any field that should only be one of a set of choices.
    """
    def __init__(self, choices):
        self.choices = choices

    def emit(self, schema):
        return random.choice(self.choices)


class EmbedType(FieldType):
    """Embeds a maker as a field for nested objects."""
    def __init__(self, maker):
        self.maker = maker

    def emit(self, schema):
        return self.maker.make_one()


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


class DatetimeType(FieldType):
    """
    For date and datetime types
    """
    def __init__(self, start, end, increment=False, include_time=True):
        """
        start - minimum date
        end - maximum date
        increment - if False then make_one just returns a random date within the range
                    else a timedelta is expected and make_one would return an incrementing
                    date within the range depending on +/- of the timedelta
                    (there has got to be a better way to word this)
        include_time - date vs datetime
        """
        self.start = start
        self.end = end
        self.increment = increment
        if self.increment:
            assert isinstance(self.increment, timedelta)
        self.include_time = include_time
        self.previous_value = None

    def emit(self, schema):
        if self.increment:
            delta_force = self.increment.total_seconds()
            if self.previous_value is None:
                if delta_force > 0:
                    result = self.start
                else:
                    result = self.end
            else:
                result = self.previous_value + self.increment
            # wrap the values, if we go over or under then loop around.
            if result > self.end:
                result = self.start
            elif result < self.start:
                result = self.end
        else:
            range_delta = self.end - self.start
            delta_force = timedelta(seconds=random.randint(0, int(range_delta.total_seconds())))
            result = self.start + delta_force
        if not self.include_time:
            result = datetime(result.year, result.month, result.day)
        self.previous_value = result
        return result


class ListType(FieldType):

    def __init__(self, content_types, min_len=0, max_len=1, allow_duplicates=False):
        self.content_types = content_types
        self.min_len = min_len
        self.max_len = max_len
        self.allow_duplicates = allow_duplicates
        if not content_types:
            content_types = [StringType()]

    def emit(self, schema):
        if self.allow_duplicates:
            result = list()
            have_another = lambda x: result.append(x)
        else:
            result = set()
            have_another = lambda x: result.add(x)
        count = random.randint(self.min_len, self.max_len)
        while len(result) < count:
            type_to_make = random.choice(self.content_types)
            have_another(type_to_make.emit(schema))
        return list(result)


class ConstantField(FieldType):
    """
    A constant value
    """
    def __init__(self, value):
        self.value = value

    def emit(self, schema):
        return self.value
