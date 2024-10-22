import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def test_initialization_none(self):
        cl = CustomList()
        self.assertEqual(cl, [])

    def test_initialization_empty_iterable(self):
        cl = CustomList([])
        self.assertEqual(cl, [])

    def test_initialization_valid_iterable(self):
        cl = CustomList([1, 2, 3])
        self.assertEqual(cl, [1, 2, 3])

    def test_initialization_tuple_iterable(self):
        cl = CustomList((1, 2, 3))
        self.assertEqual(cl, [1, 2, 3])

    def test_initialization_invalid_type_err(self):
        with self.assertRaises(TypeError):
            CustomList(1)

    def test_initialization_invalid_str_err(self):
        with self.assertRaises(TypeError):
            CustomList("str")

    def test_add_cust_list_equal(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 9])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_cust_lst_list_equal(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = lst2
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 9])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_lst_cust_list_equal(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6]
        cust_list_1 = lst1
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 9])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_cust_list_left(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 3])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_cust_list_right(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6, 7]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 9, 7])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_lst_cust_list_right(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6, 7]
        cust_list_1 = lst1
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 9, 7])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_lst_cust_list_left(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5]
        cust_list_1 = lst1
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 3])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_cust_lst_list_right(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6, 7]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = lst2
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 9, 7])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_add_cust_lst_list_left(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = lst2
        result = cust_list_1 + cust_list_2
        self.assertEqual(result, [5, 7, 3])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_addition_number(self):
        lst1 = [1, 2, 3, 6]
        num = 10
        cl = CustomList(lst1)
        result = cl + num
        self.assertEqual(result, [11, 12, 13, 16])

        self.assertEqual(cl, lst1)

    def test_addition_invalid_type(self):
        lst1 = [1, 2, 3, 6]
        cl = CustomList(lst1)
        with self.assertRaises(TypeError) as cm:
            cl = cl + "string"
        self.assertEqual(
            str(cm.exception), "Cannot use operation with 'CustomList' and str"
        )

        self.assertEqual(cl, lst1)

    def test_radd_number(self):
        lst1 = [1, 2, 3, 5]
        cl = CustomList(lst1)
        result = 10 + cl
        self.assertEqual(result, [11, 12, 13, 15])

        self.assertEqual(cl, lst1)

    def test_radd_number_right(self):
        lst1 = [1, 2, 3, 5]
        cl = CustomList(lst1)
        result = cl + 10
        self.assertEqual(result, [11, 12, 13, 15])

        self.assertEqual(cl, lst1)

    def test_radd_invalid_type(self):
        lst1 = [1, 2, 3, 5]
        cl = CustomList(lst1)
        with self.assertRaises(TypeError) as cm:
            cl = "string" + cl
        self.assertEqual(
            str(cm.exception), "Cannot use operation with 'CustomList' and str"
        )

        self.assertEqual(cl, lst1)

    def test_subtraction_equal_cl(self):
        lst1 = [5, 6, 7]
        lst2 = [1, 2, 6]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 - cust_list_2
        self.assertEqual(result, [4, 4, 1])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_subtraction_equal_cl_lst(self):
        lst1 = [5, 6, 7]
        lst2 = [1, 2, 6]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = lst2
        result = cust_list_1 - cust_list_2
        self.assertEqual(result, [4, 4, 1])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_subtraction_equal_lst_cl(self):
        lst1 = [5, 6, 7]
        lst2 = [1, 2, 6]
        cust_list_1 = lst1
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 - cust_list_2
        self.assertEqual(result, [4, 4, 1])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_subtraction_iterable(self):
        lst1 = [5, 6, 7]
        lst2 = [1, 2]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        result = cust_list_1 - cust_list_2
        self.assertEqual(result, [4, 4, 7])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_subtraction_iterable_reverse(self):
        lst1 = [5, 6, 7]
        lst2 = [1, 2]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        result = cust_list_2 - cust_list_1
        self.assertEqual(result, [-4, -4, -7])

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_subtraction_lst_cust(self):
        lst1 = [5, 6, 7]
        lst2 = [1, 2]
        cust_list_1 = CustomList(lst1)
        result = cust_list_1 - lst2
        self.assertEqual(result, [4, 4, 7])

        self.assertEqual(cust_list_1, lst1)

    def test_subtraction_cust_lst(self):
        lst1 = [1, 2]
        lst2 = [5, 6, 7]
        cust_list_1 = CustomList(lst1)
        result = lst2 - cust_list_1
        self.assertEqual(result, [4, 4, 7])

        self.assertEqual(cust_list_1, lst1)

    def test_subtraction_cust_lst_less_more(self):
        lst1 = [1, 2]
        lst2 = [5, 6, 7]
        cust_list_1 = CustomList(lst1)
        result = cust_list_1 - lst2
        self.assertEqual(result, [-4, -4, -7])

        self.assertEqual(cust_list_1, lst1)

    def test_subtraction_lst_cust_less_more(self):
        lst1 = [1, 2]
        lst2 = [5, 6, 7]
        cust_list_1 = CustomList(lst2)
        result = lst1 - cust_list_1
        self.assertEqual(result, [-4, -4, -7])

        self.assertEqual(cust_list_1, lst2)

    def test_subtraction_number(self):
        lst1 = [5, 6, 7]
        cl = CustomList(lst1)
        result = cl - 2
        self.assertEqual(result, [3, 4, 5])

        self.assertEqual(cl, lst1)

    def test_subtraction_invalid_type_err(self):
        lst1 = [1, 2, 3]
        cl = CustomList(lst1)
        with self.assertRaises(TypeError):
            cl = cl - "string"
        self.assertEqual(cl, lst1)

    def test_rsub_invalid_type(self):
        lst1 = [1, 2, 3]
        cl = CustomList(lst1)
        with self.assertRaises(TypeError):
            cl = "string" - cl
        self.assertEqual(cl, lst1)

    def test_rsub_number_left(self):
        lst1 = [5, 6, 7]
        cl = CustomList(lst1)
        result = 10 - cl
        self.assertEqual(result, [5, 4, 3])

        self.assertEqual(cl, lst1)

    def test_rsub_number_right(self):
        lst1 = [5, 6, 7]
        cl = CustomList(lst1)
        result = cl - 10
        self.assertEqual(result, [-5, -4, -3])

        self.assertEqual(cl, lst1)

    def test_equality_equal_custom_lists(self):
        lst1 = [1, 2, 3]
        lst2 = [1, 2, 3]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 == cust_list_2)
        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_equality_different_custom_lists(self):

        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertFalse(cust_list_1 == cust_list_2)

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_equality_different_custom_lists_true(self):

        lst1 = [1, 6, 3]
        lst2 = [4, 1, 5]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 == cust_list_2)

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_equality_diff_size_eq_sum(self):

        lst1 = [1, 6]
        lst2 = [4, 1, 2]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 == cust_list_2)

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_inequality_equal_custom_lists(self):
        lst1 = [1, 6, 3]
        lst2 = [1, 6, 3]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertFalse(cust_list_1 != cust_list_2)

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_inequality_different_custom_lists(self):
        lst1 = [1, 2, 3]
        lst2 = [4, 5, 6]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 != cust_list_2)

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_sl_custom_list(self):
        lst1 = [1, 2, 10]
        lst2 = [3, 4, 12, 23]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 < cust_list_2)

        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_lg_custom_list(self):
        lst1 = [3, 4, 10, 11, 112, 12]
        lst2 = [1, 2]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertFalse(cust_list_1 < cust_list_2)
        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_lq_equal_custom_lists(self):
        lst1 = [1, 2, 3]
        lst2 = [1, 2, 3]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 <= cust_list_2)
        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_g_custom_list(self):
        lst1 = [3, 4]
        lst2 = [1, 2]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 > cust_list_2)
        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_gq_with_equal_custom_lists(self):
        lst1 = [1, 2, 3]
        lst2 = [1, 2, 3]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 >= cust_list_2)
        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_gq_with_noequal_custom_lists(self):
        lst1 = [1, 5]
        lst2 = [1, 2, 3]
        cust_list_1 = CustomList(lst1)
        cust_list_2 = CustomList(lst2)
        self.assertTrue(cust_list_1 >= cust_list_2)
        self.assertEqual(cust_list_1, lst1)
        self.assertEqual(cust_list_2, lst2)

    def test_string_repres(self):
        lst1 = [1, 2, 3]
        cl = CustomList(lst1)
        self.assertEqual(str(cl), "[1, 2, 3], sum=6")
        self.assertEqual(cl, lst1)


if __name__ == "__main__":
    unittest.main()
