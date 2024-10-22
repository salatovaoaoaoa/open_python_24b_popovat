from functools import wraps
import logging
from typing import Callable, List, Optional, Type

logging.basicConfig(level=logging.INFO, format="%(message)s")

SUCCES_LOG = 'run "%s" with args = %s kwargs = %s, attempt = %s, exception = %s'
ERROR_LOG = 'run "%s" with args = %s kwargs = %s, attempt = %s, exception = %s'


def retry_deco(
    restarts: Optional[int] = None,
    expect_exception: Optional[List[Type[BaseException]]] = None,
) -> Callable:

    if expect_exception is None:
        expect_exception = []

    if restarts is None:
        restarts = 1

    if not isinstance(restarts, int) or restarts < 1:
        raise ValueError(
            f"Параметр restarts должен быть int > 0, получено {restarts}"
        )

    for exc in expect_exception:
        if not isinstance(exc, type) or not issubclass(exc, BaseException):
            raise ValueError(f"{exc} не является классом исключения")

    def deco_log(function: Callable) -> Callable:
        @wraps(function)
        def function_metrics(*args, **kwargs):

            attempt = 0
            while attempt < restarts:
                attempt += 1

                try:
                    result = function(*args, **kwargs)

                    logging.info(
                        SUCCES_LOG,
                        function.__name__,
                        args,
                        kwargs,
                        attempt,
                        result,
                    )

                    return result
                except Exception as exception:
                    logging.info(
                        ERROR_LOG,
                        function.__name__,
                        args,
                        kwargs,
                        attempt,
                        type(exception).__name__,
                    )

                    is_fatal_exception = any(
                        isinstance(exception, exc) for exc in expect_exception
                    )
                    no_attempts_left = attempt == restarts

                    if is_fatal_exception or no_attempts_left:
                        raise

        return function_metrics

    return deco_log
