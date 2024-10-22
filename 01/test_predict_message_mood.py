import unittest
from unittest.mock import patch
from predict_message_mood import predict_message_mood
from some_model import SomeModel


class TestPredictMessageMood(unittest.TestCase):

    def test_invalid_input_message(self):
        with self.assertRaises(TypeError):
            predict_message_mood(
                message=[123],
                bad_thresholds=0.3,
                good_thresholds=0.8)

    def test_invalid_input_bad_thresholds(self):
        with self.assertRaises(TypeError):
            predict_message_mood(
                message="str", bad_thresholds=(1, 2), good_thresholds=0.8
            )

    def test_invalid_input_good_thresholds(self):
        with self.assertRaises(TypeError):
            predict_message_mood(
                message="str", bad_thresholds=0.5, good_thresholds=[5, 6]
            )

    def test_nan_message(self):
        with self.assertRaises(TypeError):
            predict_message_mood(
                message=None,
                bad_thresholds=0.5,
                good_thresholds=0.7)

    def test_predict_message_mood_bad_standard_input(self):
        with patch("some_model.SomeModel.predict") as mock_predict:

            mock_predict.return_value = 0.2
            test_message = "str fixed tests"

            func_mood = predict_message_mood(
                message=test_message,
            )

            mock_predict.assert_called_with(test_message)
            mock_predict.assert_called_once()

            self.assertEqual("неуд", func_mood)

    def test_predict_message_mood_norm_standard_input(self):
        with patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.5
            test_message = "str fixed tests"

            func_mood = predict_message_mood(
                message=test_message,
            )

            mock_predict.assert_called_with(test_message)
            mock_predict.assert_called_once()
            self.assertEqual("норм", func_mood)

    def test_predict_message_mood_good_standard_input(self):
        with patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.9
            test_message = "str fixed tests"

            func_mood = predict_message_mood(
                message=test_message,
            )

            mock_predict.assert_called_with(test_message)
            mock_predict.assert_called_once()
            self.assertEqual("отл", func_mood)

    def test_predict_message_mood_bad_make_input(self):
        with patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.1
            test_message = "str fixed tests"

            func_mood = predict_message_mood(
                message=test_message, bad_thresholds=0.5, good_thresholds=0.9
            )

            mock_predict.assert_called_with(test_message)
            mock_predict.assert_called_once()
            self.assertEqual("неуд", func_mood)

    def test_predict_message_mood_norm_make_input(self):
        with patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.7
            test_message = "str fixed tests"

            func_mood = predict_message_mood(
                message=test_message, bad_thresholds=0.5, good_thresholds=0.9
            )

            mock_predict.assert_called_with(test_message)
            mock_predict.assert_called_once()
            self.assertEqual("норм", func_mood)

    def test_predict_message_mood_good_make_input(self):
        with patch("some_model.SomeModel.predict") as mock_predict:
            mock_predict.return_value = 0.99
            test_message = "str fixed tests"

            func_mood = predict_message_mood(
                message=test_message, bad_thresholds=0.5, good_thresholds=0.9
            )

            mock_predict.assert_called_with(test_message)
            mock_predict.assert_called_once()
            self.assertEqual("отл", func_mood)

    @patch.object(SomeModel, "predict")
    def test_predict(self, mock_predict):
        mock_predict.return_value = 0.5
        test_message = "Исправленный (добавленный) тест"

        mood = predict_message_mood(
            message=test_message, bad_thresholds=0.3, good_thresholds=0.8
        )
        mock_predict.assert_called_with(test_message)
        mock_predict.assert_called_once()
        self.assertEqual(mood, "норм")

    @patch.object(SomeModel, "predict")
    def test_predict_bpundary_bad(self, mock_predict):
        mock_predict.return_value = 0.5
        test_message = "Исправленный (добавленный) тест"

        mood = predict_message_mood(
            message=test_message, bad_thresholds=0.5, good_thresholds=0.8
        )
        mock_predict.assert_called_with(test_message)
        mock_predict.assert_called_once()
        self.assertEqual(mood, "норм")

    @patch.object(SomeModel, "predict")
    def test_predict_bpundary_good(self, mock_predict):
        mock_predict.return_value = 0.8
        test_message = "Исправленный (добавленный) тест"

        mood = predict_message_mood(
            message=test_message, bad_thresholds=0.5, good_thresholds=0.8
        )
        mock_predict.assert_called_with(test_message)
        mock_predict.assert_called_once()
        self.assertEqual(mood, "норм")

    @patch.object(SomeModel, "predict")
    def test_predict_bpundary_good_more(self, mock_predict):
        mock_predict.return_value = 0.8000001
        test_message = "Исправленный (добавленный) тест"

        mood = predict_message_mood(
            message=test_message, bad_thresholds=0.5, good_thresholds=0.8
        )
        mock_predict.assert_called_with(test_message)
        mock_predict.assert_called_once()
        self.assertEqual(mood, "отл")

    @patch.object(SomeModel, "predict")
    def test_predict_bpundary_good_less(self, mock_predict):
        mock_predict.return_value = 0.7999999999999
        test_message = "Исправленный (добавленный) тест"

        mood = predict_message_mood(
            message=test_message, bad_thresholds=0.5, good_thresholds=0.8
        )
        mock_predict.assert_called_with(test_message)
        mock_predict.assert_called_once()
        self.assertEqual(mood, "норм")

    @patch.object(SomeModel, "predict")
    def test_predict_bpundary_bad_less(self, mock_predict):
        mock_predict.return_value = 0.4999999999999
        test_message = "Исправленный (добавленный) тест"

        mood = predict_message_mood(
            message=test_message, bad_thresholds=0.5, good_thresholds=0.8
        )
        mock_predict.assert_called_with(test_message)
        mock_predict.assert_called_once()
        self.assertEqual(mood, "неуд")

    @patch.object(SomeModel, "predict")
    def test_predict_bpundary_bad_more(self, mock_predict):
        mock_predict.return_value = 0.5000001
        test_message = "Исправленный (добавленный) тест"

        mood = predict_message_mood(
            message=test_message, bad_thresholds=0.5, good_thresholds=0.8
        )
        mock_predict.assert_called_with(test_message)
        mock_predict.assert_called_once()
        self.assertEqual(mood, "норм")


if __name__ == "__main__":
    unittest.main()
