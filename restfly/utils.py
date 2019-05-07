'''
Utils
=====

.. autofunction:: dict_merge
.. autofunction:: force_case
.. autofunction:: trunc

'''
import re

def dict_merge(master, updates):
    '''
    Merge 2 dictionaries together  The updates dictionary will be merged into
    the master, adding/updating any values as needed.

    Args:
        master (dict): The master dictionary to be used as the base.
        updates (dict): The dictionary that will overload the values in the master.

    Returns:
        :obj:`dict`:
            The merged dictionary

    Examples:
        >>> a = {'one': 1, 'two': 2, 'three': {'four': 4}}
        >>> b = {'a': 'a', 'three': {'b': 'b'}}
        >>> dict_merge(a, b)
        {'a': 'a', 'one': 1, 'two': 2, 'three': {'b': b, 'four': 4}}
    '''
    for key in updates:
        if key in master and isinstance(master[key], dict) and isinstance(updates[key], dict):
            master[key] = dict_merge(master[key], updates[key])
        else:
            master[key] = updates[key]
    return master


def force_case(obj, case):
    '''
    A simple case enforcement function.

    Args:
        obj (Object): object to attempt to enforce the case upon.

    Returns:
        :obj:`obj`:
            The modified object

    Examples:
        A list of mixed types:

        >>> a = ['a', 'list', 'of', 'strings', 'with', 'a', 1]
        >>> force_Case(a, 'upper')
        ['A', 'LIST', 'OF', 'STRINGS', 'WITH', 'A', 1]

        A simple string:

        >>> force_case('This is a TEST', 'lower')
        'this is a test'

        A non-string item that'll pass through:

        >>> force_case(1, 'upper')
        1
    '''
    if case == 'lower':
        if isinstance(obj, list):
            return [i.lower() for i in obj if isinstance(i, str)]
        elif isinstance(obj, str):
            return obj.lower()

    elif case == 'upper':
        if isinstance(obj, list):
            return [i.upper() for i in obj if isinstance(i, str)]
        elif isinstance(obj, str):
            return obj.upper()

    return obj


def trunc(text, limit, suffix='...'):
    '''
    Truncates a string to a given number of characters.  If a string extends
    beyond the limit, then truncate and add an ellipses after the truncation.

    Args:
        text (str): The string to truncate
        limit (int): The maximum limit that the string can be.
        suffix (str):
            What suffix should be appended to the truncated string when we
            truncate?  If left unspecified, it will default to ``...``.


    Returns:
        :obj:`str`:
            The truncated string

    Examples:
        A simple truncation:

        >>> trunc('this is a test', 6)
        'thi...'

        Truncating with no suffix:

        >>> trunc('this is a test', 6, suffix=None)
        'this i'

        Truncating with a custom suffix:

        >>> trunc('this is a test', 6, suffix='->')
        'this->'
    '''
    if len(text) >= limit:
        if isinstance(suffix, str):
            # If we have a suffix, then reduce the text string length further by
            # the length of the suffix and then concatenate both the text and
            # suffix together.
            return '{}{}'.format(text[: limit - len(suffix)], suffix)
        else:
            # If no suffix, then simply reduce the string size.
            return text[:limit]
    return text