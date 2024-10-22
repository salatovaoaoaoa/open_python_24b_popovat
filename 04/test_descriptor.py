import unittest
from descriptor import WeddingData, Base, String, Integer, PositiveFloat


class TestBase(unittest.TestCase):
    def setUp(self):
        class TestExample:
            attr = Base()

        self.example = TestExample()

    def test_get_no_object(self):
        f = Base().__get__
        self.assertIsNone(f(None, None))

    def test_set_no_object(self):
        f = Base().__set__
        self.assertIsNone(f(None, "value"))

    def test_delete_not_object(self):
        f = Base().__delete__
        self.assertIsNone(f(None))

    def test_validate_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            Base().validate("test")


class TestString(unittest.TestCase):
    def setUp(self):
        class TestExample:
            name = String()

        self.example = TestExample()

    def test_valid_string(self):
        self.example.name = "Tatiana"
        self.assertEqual(self.example.name, "Tatiana")

    def test_empty_string(self):
        with self.assertRaises(ValueError):
            self.example.name = ""

    def test_whitespace_string(self):
        with self.assertRaises(ValueError):
            self.example.name = "    "

    def test_not_string(self):
        with self.assertRaises(ValueError):
            self.example.name = 123


class TestInteger(unittest.TestCase):
    def setUp(self):
        class TestExample:
            guests = Integer()

        self.example = TestExample()

    def test_valid_integer(self):
        self.example.guests = 100
        self.assertEqual(self.example.guests, 100)

    def test_non_integer(self):
        with self.assertRaises(ValueError):
            self.example.guests = "100"


class TestPositiveFloat(unittest.TestCase):
    def setUp(self):
        class TestExample:
            budget = PositiveFloat()

        self.example = TestExample()

    def test_valid_float(self):
        self.example.budget = 100.50
        self.assertEqual(self.example.budget, 100.50)

    def test_non_float(self):
        with self.assertRaises(ValueError):
            self.example.budget = 100

    def test_negative_float(self):
        with self.assertRaises(ValueError):
            self.example.budget = -100.50

    def test_zero_float(self):
        with self.assertRaises(ValueError):
            self.example.budget = 0.0


class TestWeddingData(unittest.TestCase):
    def test_valid_wedding_data(self):
        valid_data = WeddingData(
            counter=5,
            money=1000.50,
            name="Tatiana",
        )
        self.assertEqual(valid_data.counter, 5)
        self.assertEqual(valid_data.money, 1000.50)
        self.assertEqual(valid_data.name, "Tatiana")

    def test_invalid_counter(self):
        with self.assertRaises(ValueError):
            WeddingData(
                counter="not an int",
                money=1000.50,
                name="Tatiana",
            )

    def test_invalid_money(self):
        with self.assertRaises(ValueError):
            WeddingData(
                counter=5,
                money="not a float",
                name="Tatiana",
            )

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            WeddingData(
                counter=5,
                money=1000.50,
                name="",
            )


if __name__ == "__main__":
    unittest.main()
