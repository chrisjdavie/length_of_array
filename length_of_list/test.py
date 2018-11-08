from unittest import TestCase
from unittest.mock import patch

from parameterized import parameterized

from length_of_list.length_of_list import find_upper_lower_bounds_list


class TestFindUpperLowerBoundsList(TestCase):

    @parameterized.expand([(0, 0, 1), (2, 1, 2), (11, 8, 16)])
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
