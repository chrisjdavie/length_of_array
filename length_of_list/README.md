# Length of list

Problem description:

"Count the number of elements in a list without using count, size or length operators (or their equivalents). Assume the list only can be asked for an element at a certain position, make sure this is efficient for extreme large lists as well."

I have assumed additionally this list is aasked for the value at index `i` via `value = <list>[i]` will raise `IndexError` when an invalid index is asked for (consistent with Python lists).

## How to run

Requires Python 3.X (tested with 3.6 and 3.7). The tests require parameterized 
to be installed

`pip install parameterized`

Tests are in `length_of_list/tests.py`, and can be run with the command (from
the parent directory of this one)

`python -m unittest length_of_list/tests.py`

## Comments on approach

An efficient algorithm for finding the length `N` of a list with lower than an 
arbitrary bound is a binary search (time complexity `O(logN)`). This will work
with quite large numbers (log2(trillion) ~ 40), likely running out of storage
space for the list before we run out of time to find the length.

In this case, the upper bound is not specified. Consistent with the time 
complexity of the search, if we check that every 2^i (i=0,1,2...) is valid,
we can find an upper bound (the first invalid index) in `O(logN)` time, not
taking more time than the binary search. 

With this upper bound found, we can then use the binary search to find the 
length of the list. 

(Additionally, the search provides a lower limit, the previous step that
hasn't been used. I have used this in the algorithm but just using the upper
bound doesn't change the time complexity, it saves 2 checks.)
