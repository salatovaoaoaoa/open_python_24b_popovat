import unittest
import os
import io
from generator import generator

current_directory = os.getcwd()


class TestGenerator(unittest.TestCase):

    test_file_name = "test_text.txt"
    file_path = os.path.join(current_directory, test_file_name)

    def setUp(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write("а Роза упала на лапу Азора\n")
            file.write("а Роза упала на голову Азора\n")
            file.write("а Роза упала на ногу Азора\n")
            file.write("курс Углубленный питон\n")
            file.write("Углубленный питон\n")
            file.write("курс питон\n")
            file.write("Спасибо за лекции мне все очень нравится\n")
            file.write("Изучаю работу генераторов мир таков\n")
            file.write("Привет мир таков\n")
            file.write("Пока мир таков\n")
            file.write("Это уникальная строка таких слов больше нет\n")
            file.write("совпадения строки поиска с целой строкой в файле\n")
            file.write("совпадение нескольких фильтров одной строке\n")
            file.write("Стоп слово есть\n")
            file.write("Стоп слово нет\n")
            file.write("Попытка\n")

    def tearDown(self):
        os.remove(self.file_path)

    def test_io_object(self):
        file_name = io.StringIO(
            "Изучаю работу генераторов мир таков\nПока мир таков\n"
        )
        match_words = ["Изучаю", "работу"]
        stop_words = ["таковd"]

        result = list(generator(file_name, match_words, stop_words))
        self.assertEqual(result, ["Изучаю работу генераторов мир таков"])

    def test_invalid_file_name_type(self):
        match_words = ["Роза", "питон"]
        stop_words = ["таков"]

        with self.assertRaises(
            TypeError,
            msg="Не удается прочесть переданный объект."
        ):
            list(generator(123, match_words, stop_words))

    def test_empty_file(self):
        empty_file = io.StringIO("")
        result = list(
            generator(
                empty_file,
                match_words=["word"],
                stop_words=["stop"]
                )
            )
        self.assertEqual(result, [])

    def test_type_error_match_words_not_list(self):
        with self.assertRaises(TypeError):
            list(
                generator(
                    file=self.file_path,
                    match_words=(1, 2, "str"),
                    stop_words=["мир", "hello", "str"],
                )
            )

    def test_type_error_stop_words_not_list(self):
        with self.assertRaises(TypeError):
            list(
                generator(
                    file=self.file_path,
                    match_words=["мир", "hello", "str"],
                    stop_words=(1, 2, "str"),
                )
            )

    def test_type_error_match_words_in_list(self):
        with self.assertRaises(TypeError):
            list(
                generator(
                    file=self.file_path,
                    match_words=[1, 2, "str"],
                    stop_words=["мир", "hello", "str"],
                )
            )

    def test_type_error_stop_words_in_list(self):
        with self.assertRaises(TypeError):
            list(
                generator(
                    file=self.file_path,
                    match_words=["мир", "hello", "str"],
                    stop_words=[1, 2, "str"],
                )
            )

    def test_eq_find_stop_to_str(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Попытка"],
                stop_words=["попытка"]
            )
        )
        self.assertEqual(result, [])

    def test_eq_find_no_stop_to_str(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Попытка"],
                stop_words=["Покkа"]
            )
        )
        self.assertEqual(result, ["Попытка"])

    def test_eq_find_empt_stop_to_str(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Попытка"],
                stop_words=[]
            )
        )
        self.assertEqual(result, ["Попытка"])

    def test_eq_no_find_stop_to_str(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Покkа"],
                stop_words=["попытка"]
            )
        )
        self.assertEqual(result, [])

    def test_eq_empt_find_stop_to_str(self):
        result = list(
            generator(
                self.file_path,
                match_words=[],
                stop_words=["попытка"]
            )
        )
        self.assertEqual(result, [])

    def test_generator_with_matching_word(self):
        result = list(
            generator(
                self.file_path,
                match_words=["роза"],
                stop_words=["питон"]
            )
        )
        self.assertEqual(
            result,
            [
                "а Роза упала на лапу Азора",
                "а Роза упала на голову Азора",
                "а Роза упала на ногу Азора",
            ],
        )

    def test_generator_with_stop_word(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Углубленный"],
                stop_words=["курс"]
                )
        )
        self.assertEqual(result, ["Углубленный питон"])

    def test_generator_no_matches(self):
        result = list(
            generator(self.file_path, match_words=["ароза"], stop_words=["мир"])
        )
        self.assertEqual(result, [])

    def test_generator_skip(self):
        result = list(
            generator(
                self.file_path,
                match_words=["мир"],
                stop_words=["работу", "привет", "пока"],
            )
        )
        self.assertEqual(result, [])

    def test_generator_with_multiple_words(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Углубленный", "работу"],
                stop_words=["мир"],
            )
        )
        self.assertEqual(
            result,
            ["курс Углубленный питон", "Углубленный питон"]
        )

    def test_generator_with_stop_find_in_one_row(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Это", "уникальная"],
                stop_words=["строка"],
            )
        )
        self.assertEqual(result, [])

    def test_equal_str_find(self):
        result = list(
            generator(
                self.file_path,
                match_words=[
                    "совпадения строки поиска с целой строкой в файле"
                    ],
                stop_words=["строка"],
            )
        )
        self.assertEqual(result, [])

    def test_equal_sep_str_find(self):
        result = list(
            generator(
                self.file_path,
                match_words=[
                    "совпадения",
                    "строки",
                    "поиска",
                    "с",
                    "целой",
                    "строкой",
                    "в",
                    "файле",
                ],
                stop_words=["строка"],
            )
        )
        self.assertEqual(
            result,
            ["совпадения строки поиска с целой строкой в файле"]
            )

    def test_equal_str_stop(self):
        result = list(
            generator(
                self.file_path,
                match_words=["find"],
                stop_words=["совпадения строки поиска с целой строкой в файле"],
            )
        )
        self.assertEqual(result, [])

    def test_equal_sep_str_stop(self):
        result = list(
            generator(
                self.file_path,
                match_words=["find"],
                stop_words=[
                    "совпадения",
                    "строки",
                    "поиска",
                    "с",
                    "целой",
                    "строкой",
                    "в",
                    "файле",
                ],
            )
        )
        self.assertEqual(result, [])

    def test_identical_match_and_stop_words(self):
        result = list(
            generator(
                self.file_path,
                match_words=["питон"],
                stop_words=["питон"]
            )
        )
        self.assertEqual(result, [])

    def test_equal_sep_str_stop_find(self):
        result = list(
            generator(
                self.file_path,
                match_words=[
                    "совпадения",
                    "строки",
                    "поиска",
                    "с",
                    "целой",
                    "строкой",
                    "в",
                    "файле",
                ],
                stop_words=[
                    "совпадения",
                    "строки",
                    "поиска",
                    "с",
                    "целой",
                    "строкой",
                    "в",
                    "файле",
                ],
            )
        )
        self.assertEqual(result, [])

    def test_some_filter_in_one_str(self):
        result = list(
            generator(
                self.file_path,
                match_words=["совпадение", "нескольких", "одной"],
                stop_words=[],
            )
        )
        self.assertEqual(
            result,
            ["совпадение нескольких фильтров одной строке"]
            )

    def test_no_match_with_stop_word(self):
        result = list(
            generator(self.file_path, match_words=["Роза"], stop_words=["Роза"])
        )
        self.assertEqual(result, [])

    def test_partial_match(self):
        result = list(
            generator(
                self.file_path,
                match_words=["курс"],
                stop_words=[])
            )
        self.assertEqual(result, ["курс Углубленный питон", "курс питон"])

    def test_not_full_word_match(self):
        result = list(
            generator(
                self.file_path,
                match_words=["кур"],
                stop_words=[]
                )
            )
        self.assertEqual(result, [])

    def test_insensitivity(self):
        result = list(
            generator(
                self.file_path,
                match_words=["роза"],
                stop_words=[]
                )
            )
        self.assertEqual(
            result,
            [
                "а Роза упала на лапу Азора",
                "а Роза упала на голову Азора",
                "а Роза упала на ногу Азора",
            ],
        )

    def test_multiple_matches_in_one_line(self):
        result = list(
            generator(
                self.file_path,
                match_words=["мир", "таков"],
                stop_words=[]
            )
        )
        self.assertEqual(
            result,
            [
                "Изучаю работу генераторов мир таков",
                "Привет мир таков",
                "Пока мир таков",
            ],
        )

    def test_filter_words_with_special_characters(self):
        result = list(
            generator(self.file_path, match_words=["курс"], stop_words=["курс"])
        )
        self.assertEqual(result, [])

    def test_single_match_word_and_empty_stop_words(self):
        result = list(
            generator(
                self.file_path,
                match_words=["это"],
                stop_words=[]
            )
        )
        self.assertEqual(
            result,
            ["Это уникальная строка таких слов больше нет"]
        )

    def test_long_stop_word(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Стоп"],
                stop_words=["Стоп слово"]
            )
        )
        self.assertEqual(result, ["Стоп слово есть", "Стоп слово нет"])

    def test_long_stop_word_sep(self):
        result = list(
            generator(
                self.file_path,
                match_words=["Стоп"],
                stop_words=["стоп", "слово"]
            )
        )
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
