from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from length_of_list.length_of_list import find_upper_lower_bounds_list, \
    find_list_length_between_bounds, length_of_list


class TestLengthOfList(TestCase):
    """Test full run"""

    @parameterized.expand(((i,) for i in range(20)))
    def test(self, list_length):

        target_list = [1] * list_length
        self.assertEqual(list_length, length_of_list(target_list))


LIST_LENGTHS_WITH_UPPER_LOWER_BOUNDS = [
    (0, 0, 1), (1, 0, 1), (2, 1, 2), (11, 8, 16)]


class TestFindUpperLowerBoundsList(TestCase):

    @parameterized.expand(LIST_LENGTHS_WITH_UPPER_LOWER_BOUNDS)
    def test(self, list_length, expected_lower_bound, expected_upper_bound):

        target_list = [1] * list_length

        lower_bound, upper_bound = find_upper_lower_bounds_list(target_list)

        self.assertEqual(expected_lower_bound, lower_bound)
        self.assertEqual(expected_upper_bound, upper_bound)

    def test_raises_when_exceeds_loop_limit(self):

        patched_loop_limit = 2
        with patch("length_of_list.length_of_list.LOOP_LIMIT",
                   patched_loop_limit):
            target_list = [1] * (2 ** (patched_loop_limit - 1) + 1)
            with self.assertRaises(ValueError):
                find_upper_lower_bounds_list(target_list)


class TestFindListLengthBetweenBounds(TestCase):

    @parameterized.expand(LIST_LENGTHS_WITH_UPPER_LOWER_BOUNDS)
    def test(self, list_length, lower_bound, upper_bound):
        target_list = [1] * list_length

        reported_list_length = find_list_length_between_bounds(
            target_list, lower_bound, upper_bound)

        self.assertEqual(reported_list_length, list_length)

    def test_raises_when_exceeds_loop_limit(self):

        target_list = [1] * 11
        lower_bound = 8
        upper_bound = 16

        patched_loop_limit = 1
        with patch("length_of_list.length_of_list.LOOP_LIMIT",
                   patched_loop_limit):
            with self.assertRaises(ValueError):
                find_list_length_between_bounds(
                    target_list, lower_bound, upper_bound)
