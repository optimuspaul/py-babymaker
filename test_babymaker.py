from babymaker import BabyMaker, EnumType, IntType, StringType, UUIDType, FieldType
import unittest
import string
import sys


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
        self.assertIsInstance(the_id, long)

    def test_uuid_field_int_str_format(self):
        fields = {
            "id": UUIDType("int_str")
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        for char in the_id:
            self.assertTrue(char in string.digits)
        will_it_blend = long(the_id)

    def test_int_field(self):
        fields = {
            "id": IntType(min_value=10, max_value=11)
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, (int, long))
        self.assertTrue(the_id >= 10)
        self.assertTrue(the_id <= 11)
        fields = {
            "id": IntType()
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, (int, long))
        self.assertTrue(the_id >= 0)
        self.assertTrue(the_id <= sys.maxint)

    def test_string_field(self):
        fields = {
            "id": StringType(min_size=10, max_size=22)
        }
        female_of_the_species = BabyMaker(fields)
        one = female_of_the_species.make_one()
        the_id = one.get("id")
        self.assertIsInstance(the_id, basestring)
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
        self.assertIsInstance(the_id, basestring)
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
        self.assertIsInstance(the_id, basestring)
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


