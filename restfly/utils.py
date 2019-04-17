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


def validate(name, obj, expected_type,
             choices=None, default=None, case=None, pattern=None):
    '''
    Internal function for validating that inputs we are receiving are of
    the right type, have the expected values, and can handle defaults as
    necessary.

    Args:
        name (str): The name of the object (for exception reporting)
        obj (obj): The object that we will be checking
        expected_type (type):
            The expected type of object that we will check against.
        choices (list, optional):
            if the object is only expected to have a finite number of values
            then we can check to make sure that our input is one of these
            values.
        default (obj, optional):
            if we want to return a default setting if the object is None,
            we can set one here.
        case (string, optional):
            if we want to force the object values to be upper or lower case,
            then we will want to set this to either ``upper`` or ``lower``
            depending on the desired outcome.  The returned object will then
            also be in the specified case.
        pattern (string, optional):
            If we want to validate the input based on a regex pattern, then
            we should specify one here.

    Returns:
            obj: Either the object or the default object depending.
    '''
    # Enforce the object case if specified.
    obj = force_case(obj, case)
    choices = force_case(choices, case)
    default = force_case(default, case)

    # If the object sent to us has a None value, then we will return the
    # default value.
    if obj == None:
        return default

    # If the expected_type parameter is not a tuple, then we will wrap it as
    # a single-item tuple.
    if not isinstance(expected_type, tuple):
        expected_type = tuple(expected_type)

    # If we are checking for a string type, we will also want to check for
    # unicode type transparently, so add the unicode type to the expected
    # types list.  Please note that this is for Python2 only, as Python3 treats
    # all strings as type string.
    try:
        if str in expected_type:
            expected_type = expected_type + (unicode)
    except NameError:
        pass


    # Check to see if the instance is one of the expected types.  If it isn't,
    # then we will want to raise a TypeError and inform the user of what has
    # transpired.
    if not isinstance(obj, expected_type):
        raise TypeError('{} is of type {}.  Expected {}.'.format(
            name, obj.__class__.__name__, expected_type))

    # If the type is of "uuid", then we will specify a pattern and then
    # overload the type to be a type of str.
    if 'uuid' in etypes:
        pattern = r'^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$'
        etypes[etypes.index('uuid')] = str

    # If the object is none of the right types then we want to raise a
    # TypeError as it was something we weren't expecting.
    if not type_pass:
        raise TypeError('{} is of type {}.  Expected {}.'.format(
            name,
            obj.__class__.__name__,
            expected_type.__name__ if hasattr(expected_type, '__name__') else expected_type
        ))

    # if the object is only expected to have one of a finite set of values,
    # we should check against that and raise an exception if the the actual
    # value is outside of what we expect.

    if isinstance(obj, list):
        for item in obj:
            if isinstance(choices, list) and item not in choices:
                raise UnexpectedValueError(
                    '{} has value of {}.  Expected one of {}'.format(
                        name, obj, ','.join([str(i) for i in choices])
                ))
    elif isinstance(choices, list) and obj not in choices:
        raise UnexpectedValueError(
            '{} has value of {}.  Expected one of {}'.format(
                name, obj, ','.join([str(i) for i in choices])
        ))

    if pattern and isinstance(obj, str):
        if len(re.findall(pattern, str(obj))) <= 0:
            raise UnexpectedValueError(
                '{} has value of {}.  Does not match pattern {}'.format(
                    name, obj, pattern)
            )


    # if we made it this fire without an exception being raised, then assume
    # everything is good to go and return the object passed to us initially.
    return obj