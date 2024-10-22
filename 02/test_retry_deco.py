import unittest
from unittest.mock import patch, call, Mock
from retry_deco import retry_deco

SUCCES_LOG = 'run "%s" with args = %s kwargs = %s, attempt = %s, exception = %s'
ERROR_LOG = 'run "%s" with args = %s kwargs = %s, attempt = %s, exception = %s'


class TestRetryDeco(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('logging.info')
        self.log_func_mock = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_success_no_args(self):

        @retry_deco()
        def test(a, b):
            return a + b

        result = test(1, 2)

        self.assertEqual(result, 3)

        expected_calls = [
            call.logging.info(
                SUCCES_LOG,
                test.__name__,
                (1, 2),
                {},
                1,
                result
            )
        ]

        self.assertEqual(
            self.log_func_mock.mock_calls,
            expected_calls
        )

    def test_failure_no_args(self):

        @retry_deco()
        def test(a, b):
            return a / b

        try:
            test(1, 0)
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)

        expected_calls = [
            call.logging.info(
                ERROR_LOG,
                test.__name__,
                (1, 0),
                {},
                1,
                ZeroDivisionError.__name__
            )
        ]

        self.assertEqual(
            self.log_func_mock.mock_calls,
            expected_calls
        )

    def test_success_multiple_restarts(self):

        @retry_deco(3)
        def test(a, b):
            return a + b

        result = test(1, 2)

        self.assertEqual(result, 3)

        expected_calls = [
            call.logging.info(
                SUCCES_LOG,
                test.__name__,
                (1, 2),
                {},
                1,
                result
            )
        ]

        self.assertEqual(
            self.log_func_mock.mock_calls,
            expected_calls
        )

    def test_failure_multiple_restarts(self):

        @retry_deco(3)
        def test(a, b):
            return a / b

        try:
            test(1, 0)
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)

        expected_calls = [
            call.logging.info(
                ERROR_LOG,
                test.__name__,
                (1, 0),
                {},
                i + 1,
                ZeroDivisionError.__name__
            ) for i in range(3)
        ]

        self.assertEqual(
            self.log_func_mock.mock_calls,
            expected_calls
        )

    def test_failure_multiple_restarts_expected_error(self):

        @retry_deco(3, [ZeroDivisionError])
        def test(a, b):
            return a / b

        try:
            test(1, 0)
            self.fail()
        except Exception as e:
            self.assertIsInstance(e, ZeroDivisionError)

        expected_calls = [
            call.logging.info(
                ERROR_LOG,
                test.__name__,
                (1, 0),
                {},
                1,
                ZeroDivisionError.__name__
            )
        ]

        self.assertEqual(
            self.log_func_mock.mock_calls,
            expected_calls
        )

    def test_function_succeeds_on_retry(self):
        mock_func_for_succeeds_on_retry = Mock(
            side_effect=[RuntimeError("fail"), "success"]
        )

        @retry_deco(restarts=5, expect_exception=[ValueError])
        def func_test():
            return mock_func_for_succeeds_on_retry()

        result = func_test()
        self.assertEqual(result, "success")
        self.assertEqual(mock_func_for_succeeds_on_retry.call_count, 2)
        self.assertEqual(self.log_func_mock.call_count, 2)

    def test_invalid_restarts_zero(self):
        with self.assertRaises(ValueError) as context:

            @retry_deco(restarts=0)
            def test():
                print('OK')

        self.assertIn(
            "Параметр restarts должен быть int > 0, получено 0",
            str(context.exception)
        )

    def test_invalid_restarts_float(self):
        with self.assertRaises(ValueError) as context:

            @retry_deco(restarts=0.14)
            def test():
                print('OK')

        self.assertIn(
            "Параметр restarts должен быть int > 0, получено 0.14",
            str(context.exception)
        )

    def test_invalid_restarts_negative(self):
        with self.assertRaises(ValueError) as context:

            @retry_deco(restarts=-10)
            def test():
                print('OK')

        self.assertIn(
            "Параметр restarts должен быть int > 0, получено -10",
            str(context.exception)
        )

    def test_invalid_restarts_not_int_is_list(self):
        with self.assertRaises(ValueError) as context:

            @retry_deco(restarts=[1, 2])
            def test():
                print('OK')

        self.assertIn(
            "Параметр restarts должен быть int > 0, получено [1, 2]",
            str(context.exception)
        )

    def test_invalid_restarts_not_int_is_tuple(self):
        with self.assertRaises(ValueError) as context:

            @retry_deco(restarts=(1, 2))
            def test():
                print('OK')

        self.assertIn(
            "Параметр restarts должен быть int > 0, получено (1, 2)",
            str(context.exception)
        )

    def test_invalid_restarts_not_in_is_str(self):
        with self.assertRaises(ValueError) as context:

            @retry_deco(restarts='1,2')
            def test():
                print('OK')

        self.assertIn(
            "Параметр restarts должен быть int > 0, получено 1,2",
            str(context.exception)
        )

    def test_invalid_expect_exception_not_exception_class(self):
        with self.assertRaises(ValueError) as context:
            @retry_deco(expect_exception=["NotAnException"])
            def test():
                return "OK"

        self.assertIn(
            "NotAnException не является классом исключения",
            str(context.exception)
        )

    def test_function_raises_fatal_exception_immediately(self):
        mock_func_for_fatal_exception_immediately = Mock(
            side_effect=ValueError("fatal")
        )

        @retry_deco(restarts=3, expect_exception=[ValueError])
        def func():
            return mock_func_for_fatal_exception_immediately()

        with self.assertRaises(ValueError):
            func()
        mock_func_for_fatal_exception_immediately.assert_called_once()
        self.log_func_mock.assert_called_once()

    def test_function_raises_non_fatal_exception_retries_and_raises(self):
        mock_func = Mock(
            side_effect=RuntimeError("non-fatal")
        )

        @retry_deco(restarts=3, expect_exception=[ValueError])
        def func():
            return mock_func()

        with self.assertRaises(RuntimeError):
            func()
        self.assertEqual(mock_func.call_count, 3)
        self.assertEqual(self.log_func_mock.call_count, 3)

    def test_function_raises_non_fatal_then_fatal_exception(self):
        mock_func = Mock(
            side_effect=[RuntimeError("non-fatal"),
                         ValueError("fatal")]
        )

        @retry_deco(restarts=3, expect_exception=[ValueError])
        def func():
            return mock_func()

        with self.assertRaises(ValueError):
            func()
        self.assertEqual(mock_func.call_count, 2)
        self.assertEqual(self.log_func_mock.call_count, 2)

    def test_multiple_expect_exceptions(self):
        mock_func = Mock(
            side_effect=[TypeError("fatal_1"),
                         KeyError("fatal_2")]
        )

        @retry_deco(restarts=3, expect_exception=[TypeError, KeyError])
        def func():
            return mock_func()

        with self.assertRaises(TypeError):
            func()
        self.assertEqual(mock_func.call_count, 1)
        self.assertEqual(self.log_func_mock.call_count, 1)

    def test_retries_exhausted_without_success(self):
        mock_func = Mock(
            side_effect=[RuntimeError("fail1"),
                         RuntimeError("fail2"),
                         RuntimeError("fail3")]
        )

        @retry_deco(restarts=3, expect_exception=[ValueError])
        def func():
            return mock_func()

        with self.assertRaises(RuntimeError):
            func()
        self.assertEqual(mock_func.call_count, 3)
        self.assertEqual(self.log_func_mock.call_count, 3)


if __name__ == "__main__":
    unittest.main()
