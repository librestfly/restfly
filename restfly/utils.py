import re

def dict_merge(master, updates):
    '''
    Merge 2 dictionaries together  The updates dictionary will be merged into
    the master, adding/updating any values as needed.

    Args:
        master (dict): The master dictionary to be used as the base.
        updates (dict): The dictionary that will overload the values in the master.

    Returns:
        dict: The merged dictionary
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
        obj: The modified object
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
