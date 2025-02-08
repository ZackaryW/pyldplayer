def flatten_nested_dict(data: dict, parent_key: str = "", sep: str = ".") -> dict:
    """
    Flattens a nested dictionary into a single-level dictionary.

    Args:
        data (dict): The nested dictionary to be flattened.
        parent_key (str, optional): The parent key of the current dictionary. Defaults to ''.
        sep (str, optional): The separator used to join the parent key and the current key. Defaults to '.'.

    Returns:
        dict: The flattened dictionary.

    Example:
        >>> data = {'a': {'b': 1, 'c': {'d': 2}}}
        >>> flatten_nested_dict(data)
        {'a.b': 1, 'a.c.d': 2}
    """
    items = []
    for key, value in data.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_nested_dict(value, new_key, sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def parse_dotted_dict(data: dict):
    """
    Parses a dictionary with dotted keys into a nested dictionary.

    Args:
        data (dict): The dictionary to be parsed.

    Returns:
        dict: The parsed dictionary with nested structure.

    Example:
        >>> data = {'a.b': 1, 'a.c.d': 2}
        >>> parse_dotted_dict(data)
        {'a': {'b': 1, 'c': {'d': 2}}}
    """
    result = {}
    for key, value in data.items():
        keys = key.split(".")
        temp = result
        for k in keys[:-1]:
            temp = temp.setdefault(k, {})
        temp[keys[-1]] = value
    return result
