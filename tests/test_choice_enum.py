import unittest
from enum import Enum

from django_choice_enum import ChoiceEnum


class TestCase(unittest.TestCase):
    def setUp(self):
        class EmailType(ChoiceEnum):
            other = 0
            personal = 1  # for home
            corporate = 2  # for work

        self.EmailType = EmailType

    def test_it_is_enum_subtype(self):
        self.assertTrue(issubclass(ChoiceEnum, Enum))

    def test_it_returns_value_by_name(self):
        self.assertEqual(0, self.EmailType.other.value)
        self.assertEqual(1, self.EmailType.personal.value)
        self.assertEqual(2, self.EmailType.corporate.value)

    def test_it_returns_name(self):
        self.assertEqual('other', self.EmailType.other.name)
        self.assertEqual('personal', self.EmailType.personal.name)
        self.assertEqual('corporate', self.EmailType.corporate.name)

    def test_it_returns_inline_doc(self):
        self.assertIsNone(self.EmailType.other.__doc__)
        self.assertEqual('for home', self.EmailType.personal.__doc__)
        self.assertEqual('for work', self.EmailType.corporate.__doc__)

    def test_it_is_compatible_with_int_value(self):
        self.assertEqual(0, self.EmailType.other)
        self.assertNotEqual(1, self.EmailType.other)
        self.assertNotEqual(2, self.EmailType.other)

        self.assertNotEqual(0, self.EmailType.personal)
        self.assertEqual(1, self.EmailType.personal)
        self.assertNotEqual(2, self.EmailType.personal)

        self.assertNotEqual(0, self.EmailType.corporate)
        self.assertNotEqual(1, self.EmailType.corporate)
        self.assertEqual(2, self.EmailType.corporate)

    def test_it_is_compatible_with_str_value(self):
        self.assertEqual('other', self.EmailType.other)
        self.assertNotEqual('personal', self.EmailType.other)
        self.assertNotEqual('corporate', self.EmailType.other)

        self.assertNotEqual('other', self.EmailType.personal)
        self.assertEqual('personal', self.EmailType.personal)
        self.assertNotEqual('corporate', self.EmailType.personal)

        self.assertNotEqual('other', self.EmailType.corporate)
        self.assertNotEqual('personal', self.EmailType.corporate)
        self.assertEqual('corporate', self.EmailType.corporate)

    def test_it_is_compatible_with_enum_value(self):
        self.assertEqual(self.EmailType.other, self.EmailType.other)
        self.assertNotEqual(self.EmailType.personal, self.EmailType.other)
        self.assertNotEqual(self.EmailType.corporate, self.EmailType.other)

        self.assertNotEqual(self.EmailType.other, self.EmailType.personal)
        self.assertEqual(self.EmailType.personal, self.EmailType.personal)
        self.assertNotEqual(self.EmailType.corporate, self.EmailType.personal)

        self.assertNotEqual(self.EmailType.other, self.EmailType.corporate)
        self.assertNotEqual(self.EmailType.personal, self.EmailType.corporate)
        self.assertEqual(self.EmailType.corporate, self.EmailType.corporate)

    def test_items_method_returns_dict_like_list(self):
        d = dict(self.EmailType.items())

        self.assertDictEqual({
            'other': 0,
            'personal': 1,
            'corporate': 2,
        }, d)

    def test_choices_property_returns_dict_like_list(self):
        d = dict(self.EmailType.choices)

        self.assertDictEqual({
            0: 'other',
            1: 'personal (for home)',
            2: 'corporate (for work)',
        }, d)

    def test_it_can_be_represented(self):
        self.assertEqual(
            "EmailType(('other', 0), ('personal', 1), ('corporate', 2))",
            repr(self.EmailType)
        )


if __name__ == '__main__':
    unittest.main()
