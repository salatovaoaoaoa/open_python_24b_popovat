import unittest
from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):

    def test_add_prefix(self):
        self.assertEqual(
            CustomMeta.add_prefix("some_name"), "custom_some_name"
        )

        self.assertEqual(
            CustomMeta.add_prefix("__dict__"), "__dict__"
        )

    def test_override_setattr(self):
        class TestClass(metaclass=CustomMeta):
            def __init__(self, name):
                self.name = name
                self.age = None

            @property
            def custom_name(self):
                return self.name

            def set_age(self, age):
                self.age = age

            def get_age(self):
                return self.custom_age

        obj = TestClass("blabla")

        with self.assertRaises(AttributeError):
            _ = obj.name

        self.assertEqual(obj.custom_name, "blabla")

        obj.custom_set_age(25)
        self.assertEqual(obj.custom_get_age(), 25)

    def test_new_namespace(self):
        class TestExample(metaclass=CustomMeta):
            def method(self):
                return "method_result"

            def custom_method(self):
                return self.method()

        obj = TestExample()

        with self.assertRaises(AttributeError):
            _ = obj.method()

        self.assertEqual(obj.custom_method(), "method_result")

    def test_init_override(self):
        class Example(metaclass=CustomMeta):
            def __init__(self, attr1, attr2):
                self.attr1 = attr1
                self.attr2 = attr2

            @property
            def custom_attr1(self):
                return self.attr1

            @property
            def custom_attr2(self):
                return self.attr2

            def display_attrs(self):
                return self.custom_attr1, self.custom_attr2

        obj = Example("value1", "value2")

        with self.assertRaises(AttributeError):
            _ = obj.attr1

        self.assertEqual(obj.custom_attr1, "value1")
        self.assertEqual(obj.custom_attr2, "value2")
        self.assertEqual(obj.custom_display_attrs(), ("value1", "value2"))

    def test_special_methods(self):
        class SpecialMethods(metaclass=CustomMeta):
            def __str__(self):
                return "Custom class"

            @property
            def custom_str(self):
                return str(self)

            def describe(self):
                return f"This is a {self.custom_custom_str}"

        obj = SpecialMethods()

        self.assertEqual(str(obj), "Custom class")
        self.assertEqual(obj.custom_describe(), "This is a Custom class")


if __name__ == "__main__":
    unittest.main()
