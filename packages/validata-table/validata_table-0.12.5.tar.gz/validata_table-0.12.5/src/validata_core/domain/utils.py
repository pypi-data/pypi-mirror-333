def flatten(_list):
    return [
        field
        for sublist in _list
        for field in (sublist if isinstance(sublist, list) else [sublist])
    ]
