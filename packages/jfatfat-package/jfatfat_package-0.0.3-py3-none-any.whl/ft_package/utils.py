def flatten_list(nested_list):
    """Flattens a nested list."""
    return [item for sublist in nested_list for item in sublist]


def reverse_string(s):
    """Returns the reversed version of a string."""
    return s[::-1]
