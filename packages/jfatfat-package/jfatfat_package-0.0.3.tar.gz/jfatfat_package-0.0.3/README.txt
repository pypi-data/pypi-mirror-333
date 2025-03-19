ft_package

A simple Python package with useful utility functions.

Build:
run in the terminal inside the ft_package main directory: pip install build twine
run in the terminal inside the ft_package main directory: python3 -m build
run in the terminal inside the ft_package main directory: twine upload dist/* and enter this api key, to get an api key, go to your account on PyPI and generate a new api key
run in the terminal inside the ft_package main directory: pip install jfatfat-package
now, you can run the tests inside ft_package/tests/ directory

Installation:
pip install jfatfat-package

Usage:
from ft_package import count_in_list, flatten_list, reverse_string

print(count_in_list(["apple", "banana", "apple"], "apple")) # Output: 2
print(flatten_list([[1, 2], [3, 4], [5]])) # Output: [1, 2, 3, 4, 5]
print(reverse_string("hello")) # Output: "olleh"
