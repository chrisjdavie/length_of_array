"""
Finding the length of a list the only has a method for accessing data at a
given index (assuming and error when invalid indices are used)
"""
LOOP_LIMIT = 10000


def find_upper_lower_bounds_list(target_list: list) -> (int, int):
    """
    Find the upper and lower bounds of a list that can be accessed at index
    <list>[index] and throws an error on invalid incides
    """
    lower_bound = 0
    for index in range(LOOP_LIMIT):
        two_power_index = 2 ** index
        try:
            target_list[two_power_index]
            lower_bound = two_power_index
        except IndexError:
            break
    else:
        raise ValueError(
            f"Target list length exceeds maximum {2**(LOOP_LIMIT-1)}")

    return lower_bound, two_power_index
