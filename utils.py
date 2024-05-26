def find_indices(lst, condition):
    return [idx for idx, elem in enumerate(lst) if condition(elem)]
