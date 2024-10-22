import unittest
from unittest.mock import Mock
import json
from process_json import process_json


class TestProcessJson(unittest.TestCase):

    def setUp(self):
        self.mock_callback = Mock()

    def test_required_keys_none(self):
        with self.assertRaises(ValueError) as context:
            json_str = json.dumps({"key1": "value1"})
            process_json(
                json_str=json_str,
                required_keys=None,
                tokens_find=["test"],
                callback=self.mock_callback,
            )
        self.assertIn(
            "Список ключей для поиска не задан или пуст", str(context.exception)
        )

    def test_required_keys_empty_list(self):
        with self.assertRaises(ValueError) as context:
            json_str = json.dumps({"key1": "value1"})
            process_json(
                json_str=json_str,
                required_keys=[],
                tokens_find=["test"],
                callback=self.mock_callback,
            )
        self.assertIn(
            "Список ключей для поиска не задан или пуст", str(context.exception)
        )

    def test_tokens_find_none(self):
        with self.assertRaises(ValueError) as context:
            process_json(
                json_str=json.dumps({"key1": "value1"}),
                required_keys=["key1"],
                tokens_find=None,
                callback=self.mock_callback,
            )
        self.assertIn(
            "Список токенов для поиска не задан или пуст",
            str(context.exception)
        )

    def test_tokens_find_empty_list(self):
        with self.assertRaises(ValueError) as context:
            process_json(
                json_str=json.dumps({"key1": "value1"}),
                required_keys=["key1"],
                tokens_find=[],
                callback=self.mock_callback,
            )
        self.assertIn(
            "Список токенов для поиска не задан или пуст",
            str(context.exception)
        )

    def test_callback_none(self):
        with self.assertRaises(ValueError) as context:
            process_json(
                json_str=json.dumps({"key1": "value1"}),
                required_keys=["key1"],
                tokens_find=["token"],
                callback=None,
            )
        self.assertIn("Callback функция не задана", str(context.exception))

    def test_invalid_json(self):
        with self.assertRaises(ValueError) as context:
            process_json(
                json_str='{"key": "value",}',
                required_keys=["key"],
                tokens_find=["token"],
                callback=self.mock_callback,
            )
        self.assertIn("Ошибка в формате JSON строки", str(context.exception))

    def test_not_a_json(self):
        with self.assertRaises(ValueError) as context:
            process_json(
                json_str="['key', 'value']",
                required_keys=["key"],
                tokens_find=["token"],
                callback=self.mock_callback,
            )
        self.assertIn("Ошибка в формате JSON строки", str(context.exception))

    def test_empty_json(self):
        json_str = "{}"
        process_json(
            json_str=json_str,
            required_keys=["key1", "key2"],
            tokens_find=["token"],
            callback=self.mock_callback,
        )
        self.mock_callback.assert_not_called()

    def test_empty_required_keys_set_after_unique(self):
        json_str = json.dumps({"key1": "value1"})
        process_json(
            json_str=json_str,
            required_keys=["key2", "key3"],
            tokens_find=["value1"],
            callback=self.mock_callback,
        )
        self.mock_callback.assert_not_called()

    def test_key_not_correct(self):
        json_str = json.dumps({"random_kay": "value"})
        process_json(
            json_str=json_str,
            required_keys=["key"],
            tokens_find=["value"],
            callback=self.mock_callback,
        )
        self.mock_callback.assert_not_called()

    def test_key_not_correct_val_none(self):
        json_str = json.dumps({"random_kay": None})
        process_json(
            json_str=json_str,
            required_keys=["random_kay"],
            tokens_find=["value"],
            callback=self.mock_callback,
        )
        self.mock_callback.assert_not_called()

    def test_tokens_dont_match(self):
        json_str = json.dumps({"key": "kjic"})
        process_json(
            json_str=json_str,
            required_keys=["key"],
            tokens_find=["notme"],
            callback=self.mock_callback,
        )
        self.mock_callback.assert_not_called()

    def test_one_token_match(self):
        json_str = json.dumps({"math": "pi", "russ": "pelmeni", "may": "cat"})
        process_json(
            json_str=json_str,
            required_keys=["math"],
            tokens_find=["pi"],
            callback=self.mock_callback,
        )
        self.mock_callback.assert_called_once_with("math", "pi")

    def test_some_tokens_match_for_one_key(self):
        json_str = json.dumps(
            {"math": "The sin is trigonometric funcrion like tg and cos"}
        )
        tokens = ["sin", "TG", "cOs"]
        process_json(
            json_str=json_str,
            required_keys=["math"],
            tokens_find=tokens,
            callback=self.mock_callback,
        )
        expected_calls = [
            unittest.mock.call("math", "sin"),
            unittest.mock.call("math", "tg"),
            unittest.mock.call("math", "cos"),
        ]
        self.mock_callback.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(self.mock_callback.call_count, 3)

    def test_some_keys_with_matches(self):
        json_str = json.dumps(
            {"key1": "match vAlueA", "key2": "match valueB", "key3": "No match"}
        )
        tokens = ["valuea", "valueb"]
        process_json(
            json_str=json_str,
            required_keys=["key1", "key2", "key3"],
            tokens_find=tokens,
            callback=self.mock_callback,
        )
        expected_calls = [
            unittest.mock.call("key1", "valuea"),
            unittest.mock.call("key2", "valueb"),
        ]
        self.mock_callback.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(self.mock_callback.call_count, 2)

    def test_duplicate_required_keys(self):
        json_str = json.dumps({"key": "value"})
        tokens = ["value"]
        process_json(
            json_str=json_str,
            required_keys=["key", "key", "KEY", "key1"],
            tokens_find=tokens,
            callback=self.mock_callback,
        )
        # Дубликаты ключей должны обрабатываться один раз
        self.mock_callback.assert_called_once_with("key", "value")


if __name__ == "__main__":
    unittest.main()
