from itertools import zip_longest
from typing import Iterable, Union, Callable


class CustomList(list):

    def __init__(self, iterable=None):
        if iterable is None:
            super().__init__()
        elif isinstance(iterable, Iterable) and not isinstance(iterable, str):
            super().__init__(iterable)
            if isinstance(iterable, str):
                raise TypeError(
                    "Cannot initialize CustomList with str"
                    )
        else:
            raise TypeError(
                f"Cannot initialize CustomList with {type(iterable).__name__}"
            )

    def _math_operation(self,
                        elm: Union[Iterable, int, float],
                        operation: Callable,
                        reverse=False):

        if isinstance(elm, Iterable) and not isinstance(elm, str):
            result = [
                operation(a, b) if not reverse else operation(b, a)
                for a, b in zip_longest(self, elm, fillvalue=0)
            ]
            return CustomList(result)

        if isinstance(elm, str):
            raise TypeError(
                "Cannot use operation with 'CustomList' and str"
                )

        if isinstance(elm, (int, float)):
            result = [
                operation(item, elm) if not reverse
                else operation(elm, item) for item in self
            ]
            return CustomList(result)

        raise TypeError(
            f"Operation not support for CustomList and {type(elm).__name__}"
        )

    def __add__(self, adder_elem: Union[Iterable, int, float]):
        return self._math_operation(
            adder_elem, lambda cl1, cl2: cl1 + cl2
        )

    def __radd__(self, radder_elem: Union[int, float]):
        return self._math_operation(
            radder_elem, lambda cl1, cl2: cl1 + cl2, reverse=True
        )

    def __sub__(self, sub_elem: Union[Iterable, int, float]):
        return self._math_operation(
            sub_elem, lambda cl1, cl2: cl1 - cl2
        )

    def __rsub__(self, rsub_elem: Union[Iterable, int, float]):
        return self._math_operation(
            rsub_elem, lambda cl1, cl2: cl1 - cl2, reverse=True
        )

    def _compare_eq(self, comp_expression, comp_func):
        if isinstance(comp_expression, CustomList):
            return comp_func(sum(self), sum(comp_expression))
        return super().__eq__(comp_expression)

    def __eq__(self, comp_expression):
        return self._compare_eq(comp_expression, lambda cl1, cl2: cl1 == cl2)

    def __ne__(self, comp_expression):
        return self._compare_eq(comp_expression, lambda cl1, cl2: cl1 != cl2)

    def __lt__(self, comp_expression):
        return self._compare_eq(comp_expression, lambda cl1, cl2: cl1 < cl2)

    def __le__(self, comp_expression):
        return self._compare_eq(comp_expression, lambda cl1, cl2: cl1 <= cl2)

    def __gt__(self, comp_expression):
        return self._compare_eq(comp_expression, lambda cl1, cl2: cl1 > cl2)

    def __ge__(self, comp_expression):
        return self._compare_eq(comp_expression, lambda cl1, cl2: cl1 >= cl2)

    def __str__(self):
        return f"{list(self)}, sum={sum(self)}"
