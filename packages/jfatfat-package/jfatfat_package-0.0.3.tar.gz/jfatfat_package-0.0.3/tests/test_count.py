from ft_package import count_in_list


def test_count_in_list():
    """Test the function count_in_list"""
    assert count_in_list(["a", "b", "a"], "a") == 2
    assert count_in_list([1, 2, 3, 4, 4], 4) == 2
    assert count_in_list([], "a") == 0


test_count_in_list()
print("All test succeed!")
