"""
Finding the length of a list the only has a method for accessing data at a
given index (assuming and error when invalid indices are used)
"""
from typing import Tuple

LOOP_LIMIT: int = 10000


def length_of_list(target_list: list) -> int:
    """
    Finds the length of a list.

    The 'list' can only be accessed at index <list>[index] and throws an
    IndexError on invalid incides.
    """
    upper_bound, lower_bound = find_upper_lower_bounds_list(target_list)
    return find_list_length_between_bounds(
        target_list, upper_bound, lower_bound)


def find_upper_lower_bounds_list(target_list: list) -> Tuple[int, int]:
    """
    Find the upper and lower bounds of the length of a 'list'

    The 'list' can only be accessed at index <list>[index] and throws an
    IndexError on invalid incides.
    """
    # search upwards in 2^n jumps
    lower_bound: int = 0
    for index in range(LOOP_LIMIT):
        two_power_index: int = 2 ** index
        try:
            target_list[two_power_index]
            lower_bound = two_power_index
        except IndexError:
            break
    else:
        raise ValueError(
            f"Target list length exceeds maximum {2**(LOOP_LIMIT-1)}")

    return lower_bound, two_power_index


def find_list_length_between_bounds(
        target_list: list, lower_bound: int, upper_bound: int) -> int:
    """
    Search for the length of a list within lower_bound and upper_bound.

    The 'list' can only be accessed at index <list>[index] and throws an
    IndexError on invalid incides.

    Assumes lower_bound is a valid index and upper_bound raises an exception,
    with the special case of lower_bound of 0, which can raise if the list is
    of zero length.
    """
    # Handle zero length
    if lower_bound == 0:
        try:
            target_list[lower_bound]
        except IndexError:
            return lower_bound

    # Binary search between bounds
    for _ in range(LOOP_LIMIT):
        if lower_bound + 1 == upper_bound:
            break
        midpoint: int = (lower_bound + upper_bound) // 2
        try:
            target_list[midpoint]
            lower_bound = midpoint
        except IndexError:
            upper_bound = midpoint
    else:
        raise ValueError(
            f"List length not found within maximum iterations {LOOP_LIMIT}")

    return upper_bound
