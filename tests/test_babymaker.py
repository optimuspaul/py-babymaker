from babymaker import BabyMaker, EnumType, IntType, StringType, UUIDType, FieldType, DatetimeType, FloatType, EmbedType
import unittest
import string
import sys
from datetime import datetime, timedelta


class TestMakeSomeBabies(unittest.TestCase):

    def test_make_one(self):
        fields = {
            "id": UUIDType()
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        self.assertTrue("id" in one)

    def test_make_some(self):
        fields = {
            "id": UUIDType()
        }
        female_of_the_species = BabyMaker(fields)
        some = list(female_of_the_species.make_some(8))
        self.assertEquals(len(some), 8)
        for one in some:
            self.assertTrue("id" in one)

    def test_uuid_field_hex_format(self):
        fields = {
            "id": UUIDType(format="hex_str")
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertEquals(len(the_id), 32)
        for char in the_id:
            self.assertTrue(char in string.hexdigits)

    def test_uuid_field_default_format(self):
        fields = {
            "id": UUIDType()
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertEquals(len(the_id), 36)
        for char in the_id:
            self.assertTrue(char in string.hexdigits + "-")

    def test_uuid_field_int_format(self):
        fields = {
            "id": UUIDType("int")
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, int)

    def test_uuid_field_int_str_format(self):
        fields = {
            "id": UUIDType("int_str")
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        for char in the_id:
            self.assertTrue(char in string.digits)
        will_it_blend = int(the_id)

    def test_int_field(self):
        fields = {
            "id": IntType(min_value=10, max_value=11)
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, int)
        self.assertTrue(the_id >= 10)
        self.assertTrue(the_id <= 11)
        fields = {
            "id": IntType()
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, int)
        self.assertTrue(the_id >= 0)
        self.assertTrue(the_id <= sys.maxsize)

    def test_float_field(self):
        fields = {
            "id": FloatType(min_value=2.0, max_value=10.0)
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, float)
        self.assertTrue(the_id >= 2.0)
        self.assertTrue(the_id <= 10.0)
        fields = {
            "id": FloatType()
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, float)
        self.assertTrue(the_id >= 0.0)
        self.assertTrue(the_id <= 1.0)
        for baby in female_of_the_species.make_some(100):
            the_id = baby.get("id")
            self.assertIsInstance(the_id, float)
            self.assertTrue(the_id >= 0.0)
            self.assertTrue(the_id <= 1.0)
        fields = {
            "id": FloatType(min_value=1.0)
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, float)
        self.assertTrue(the_id >= 1.0)
        self.assertTrue(the_id <= 2.0)

    def test_string_field(self):
        fields = {
            "id": StringType(min_size=10, max_size=22)
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, str)
        for char in the_id:
            self.assertTrue(char in string.printable)
        self.assertTrue(len(the_id) >= 10)
        self.assertTrue(len(the_id) <= 22)
        fields = {
            "id": StringType()
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, str)
        for char in the_id:
            self.assertTrue(char in string.printable)
        self.assertTrue(len(the_id) >= 0)
        self.assertTrue(len(the_id) <= 64)

    def test_string_field_with_limited_chars(self):
        allowed_chars = "paul"
        fields = {
            "id": StringType(allowed_chars=allowed_chars, min_size=10, max_size=22)
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, str)
        for char in the_id:
            self.assertTrue(char in allowed_chars)
        self.assertTrue(len(the_id) >= 10)
        self.assertTrue(len(the_id) <= 22)

    def test_enum_type(self):
        choices = [1, 8, "paul", 12, None]
        fields = {
            "id": EnumType(choices=choices)
        }
        female_of_the_species = BabyMaker(fields)
        some = list(female_of_the_species.make_some(88))
        self.assertEquals(len(some), 88)
        for one in some:
            the_id = one.get("id")
            self.assertTrue(the_id in choices)

    def test_base_field_type(self):
        fields = {
            "id": FieldType()
        }
        female_of_the_species = BabyMaker(fields)
        some = list(female_of_the_species.make_some(88))
        self.assertEquals(len(some), 88)
        for one in some:
            the_id = one.get("id")
            self.assertIsNone(the_id)

    def test_datetime_type(self):
        start = datetime(1976, 7, 15)
        end = datetime(1977, 7, 15)
        fields = {
            "created": DatetimeType(start, end)
        }
        female_of_the_species = BabyMaker(fields)
        some = list(female_of_the_species.make_some(88))
        self.assertEquals(len(some), 88)
        for one in some:
            created = one.get("created")
            self.assertIsInstance(created, datetime)
            self.assertTrue(created <= end)
            self.assertTrue(created >= start)

    def test_datetime_notime_type(self):
        start = datetime(1976, 7, 15)
        end = datetime(1977, 7, 15)
        fields = {
            "created": DatetimeType(start, end, include_time=False)
        }
        female_of_the_species = BabyMaker(fields)
        some = list(female_of_the_species.make_some(88))
        self.assertEquals(len(some), 88)
        for one in some:
            created = one.get("created")
            self.assertIsInstance(created, datetime)
            self.assertEquals(created.hour, 0)
            self.assertEquals(created.minute, 0)
            self.assertEquals(created.second, 0)
            self.assertTrue(created <= end)
            self.assertTrue(created >= start)

    def test_datetime_incremental_type(self):
        start = datetime(1976, 7, 15)
        end = datetime(1977, 7, 15)
        delta = timedelta(weeks=1)
        fields = {
            "created": DatetimeType(start, end, increment=delta)
        }
        female_of_the_species = BabyMaker(fields)
        some = list(female_of_the_species.make_some(56))
        self.assertEquals(len(some), 56)
        test_value = start
        for one in some:
            created = one.get("created")
            self.assertIsInstance(created, datetime)
            self.assertTrue(created <= end)
            self.assertTrue(created >= start)
            self.assertEquals(created, test_value)
            test_value += delta
            if test_value >= end:
                test_value = start

    def test_datetime_decremental_type(self):
        start = datetime(1976, 7, 15)
        end = datetime(1977, 7, 15)
        delta = timedelta(weeks=-1)
        fields = {
            "created": DatetimeType(start, end, increment=delta)
        }
        female_of_the_species = BabyMaker(fields)
        some = list(female_of_the_species.make_some(56))
        self.assertEquals(len(some), 56)
        test_value = end
        for one in some:
            created = one.get("created")
            self.assertIsInstance(created, datetime)
            self.assertTrue(created <= end)
            self.assertTrue(created >= start)
            self.assertEquals(created, test_value)
            test_value += delta
            if test_value <= start:
                test_value = end

    def test_embedded_maker(self):
        fields = {
            "id": UUIDType()
        }
        female_of_the_species = BabyMaker(fields)
        fields2 = {
            "inbed": EmbedType(female_of_the_species),
            "id": UUIDType()
        }
        grandma = BabyMaker(fields2)
        one = grandma.make_one()
        self.assertTrue("id" in one)
        self.assertTrue("inbed" in one)
        self.assertTrue("id" in one.inbed)
