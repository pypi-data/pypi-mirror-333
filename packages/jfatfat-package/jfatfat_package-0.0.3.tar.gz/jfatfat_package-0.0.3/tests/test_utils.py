from ft_package import flatten_list, reverse_string


def test_flatten_list():
    """test for function flatten_list"""
    assert flatten_list([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert flatten_list([]) == []
    assert flatten_list([[1], [2, 3], [4]]) == [1, 2, 3, 4]


def test_reverse_string():
    """test for function reverse_string"""
    assert reverse_string("hello") == "olleh"
    assert reverse_string("") == ""
    assert reverse_string("Python") == "nohtyP"


test_flatten_list()
test_reverse_string()
print("All utility function tests passed!")
