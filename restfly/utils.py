'''
Utils
=====

.. autofunction:: check
.. autofunction:: dict_clean
.. autofunction:: dict_flatten
.. autofunction:: dict_merge
.. autofunction:: force_case
.. autofunction:: trunc

'''
from .errors import UnexpectedValueError
import re, collections


def dict_flatten(d, parent_key='', sep='.'):
    '''
    Flattens a nested dict.

    Args:
        d (dict):
            The dictionary to flatten
        sep (str, optional):
            The seperation character.  If left unspecified, the default is '.'.

    Examples:
        >>> x = {'a': 1, 'b': {'c': 2}}
        >>> dict_flatten(x)
            {'a': 1, 'b.c': 2}

    Shamelessly ripped from `this <https://stackoverflow.com/a/6027615>`_
    Stackoverflow answer.
    '''
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# backwards compat with pre 1.2.
flatten = dict_flatten


def dict_clean(d):
    '''
    Recursively removes dictionary keys where the value is None

    Args:
        d (dict):
            The dictionary to clean

    Returns:
        :obj:`dict`:
            The cleaned dictionary

    Examples:
        >>> x = {'a': 1, 'b': {'c': 2, 'd': None}, 'e': None}
        >>> clean_dict(x)
            {'a': 1, 'b': {'c': 2}}
    '''
    clean = dict()
    for key, value in d.items():

        # if the value is a dictionary, then we will recursively clean.
        if isinstance(value, dict):
            new_value = dict_clean(value)
            if len(new_value.keys()) > 0:
                clean[key] = new_value

        # if the value is a list, we will check for any dictionaries within
        # the list and recursively clean.
        elif isinstance(value, list):
            new_value = list()
            for item in value:
                if isinstance(item, dict):
                    new_item = dict_clean(item)
                    if len(new_item.keys()) > 0:
                        new_value.append(new_item)
                else:
                    new_value.append(item)
            clean[key] = new_value

        # if the value isn't None, then store the value under the key.
        elif value is not None:
            clean[key] = value

    return clean


def dict_merge(master, updates):
    '''
    Merge 2 dictionaries together  The updates dictionary will be merged into
    the master, adding/updating any values as needed.

    Args:
        master (dict):
            The master dictionary to be used as the base.
        updates (dict):
            The dictionary that will overload the values in the master.

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
        if (key in master and isinstance(master[key], dict)
          and isinstance(updates[key], dict)):
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


def check(name, obj, expected_type, **kwargs):
    '''
    Check function for validating that inputs we are receiving are of the right
    type, have the expected values, and can handle defaults as necessary.

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
        case (str, optional):
            if we want to force the object values to be upper or lower case,
            then we will want to set this to either ``upper`` or ``lower``
            depending on the desired outcome.  The returned object will then
            also be in the specified case.
        pattern (str, optional):
            Specify a regex pattern from the pattern map variable.
        pattern_map (dict, optional):
            Any additional items to add to the pattern mapping.
        regex (str, optional):
            Validate that the value of the object matches this pattern.
        items_type (type, optional):
            If the expected type is an iterable, and if all of the items
            within that iterable are expected to be a given type, then
            specifying the type here will enable checking each item within
            the iterable.
            NOTE: this will traverse the iterable and return a list object.
        softcheck (bool, optional):
            If the variable is a string type

    Returns:
        :obj:`Object`:
            Either the object or the default object depending.

    Examples:
        Ensure that the value is an integer type:

        >>> check('example', val, int)

        Ensure that the value of val is within 0 and 100:

        >>> check('example', val, int, choices=list(range(100)))
    '''
    # Set the string types.
    try:
        string_types = (str, unicode)
    except NameError:
        string_types = (str)

    def validate_regex_pattern(regex, obj):
        if (isinstance(obj, string_types)
          and len(re.findall(regex, str(obj))) <= 0):
            raise UnexpectedValueError(
                '{} has value of {}.  Does not match pattern {}'.format(
                    name, obj, regex))

    def validate_choice_list(choices, obj):
        if obj not in choices:
            raise UnexpectedValueError(
                '{} has value of {}.  Expected one of {}'.format(
                    name, obj, ','.join([str(i) for i in choices])))

    def validate_expected_type(expected, obj, softcheck=True):
        if isinstance(obj, expected):
            # if everything matches, then just return the object
            return obj
        elif ((softcheck and isinstance(obj, string_types)
          and expected not in [list, tuple])):
            # if the expected type is not a list or tuple and it is a
            # string type, then we will attempt to recast the object
            # to be the expected type.
            try:
                new_obj = expected(obj)
            except:
                # if the recasting fails, then just pass through.
                raise TypeError('{} is of type {}.  Expected {}.'.format(
                    name,
                    obj.__class__.__name__,
                    expected_type.__name__
                        if hasattr(expected, '__name__') else expected)
                )
            else:
                if expected == bool:
                    # if the expected type was boolean, then we will
                    # want to ensure that the string is one of the
                    # allowed values.  From there we will set the
                    # object to be either True or False.  in either case
                    # we will also want to make sure to set the
                    # type_pass flag to ensure we don't raise a
                    # TypeError later on.
                    if obj.lower() in ['true', 'false', 'yes', 'no']:
                        return obj.lower() in ['true', 'yes']
                else:
                    # In every other case, just set the object to be the
                    # recasted object and set the type_pass flag.
                    return new_obj
        raise TypeError('{} is of type {}.  Expected {}.'.format(
            name,
            obj.__class__.__name__,
            expected_type.__name__
                if hasattr(expected, '__name__') else expected)
        )

    def validate_normalized(obj, func, arg):
        if isinstance(obj, (list, tuple)):
            # If the object is a list or tuple type, then lets ensure that
            # all of the items within the obj .
            for item in obj:
                func(arg, item)
        else:
            func(arg, obj)

    pmap = dict_merge({
        'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'hex': r'^[a-fA-f0-9]+$',
        'url': r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',
        'ipv4': r'^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$',
        'ipv6': r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))',
    }, kwargs.get('pattern_map', dict()))


    # We have a simple function to convert the case of string values so that
    # we can ensure correct output.

    # Convert the case of the inputs.
    obj = force_case(obj, kwargs.get('case'))
    kwargs['choices'] = force_case(kwargs.get('choices'), kwargs.get('case'))
    kwargs['default'] = force_case(kwargs.get('default'), kwargs.get('case'))

    # If the object sent to us has a None value, then we will return None.
    # If a default was set, then we will return the default value.
    if obj == None:
        return kwargs.get('default')

    # If we are checking for a string type, we will also want to check for
    # unicode type transparently, so add the unicode type to the expected
    # types list.  NOTE this is for Python2 only, as Python3 treats all
    # strings as type string.
    if expected_type == str:
        expected_type = string_types

    # If the object is none of the right types then we want to raise a
    # TypeError as it was something we weren't expecting.
    obj = validate_expected_type(
        expected_type, obj, kwargs.get('softcheck', True))

    if kwargs.get('items_type'):
        # If the items within the list should also be of a specific type,
        # we can check those as well
        lobj = list()
        for item in obj:
            lobj.append(validate_expected_type(
                kwargs.get('items_type'), item, kwargs.get('softcheck', True)))
        obj = lobj

    # if the object is only expected to have one of a finite set of values,
    # we should check against that and raise an exception if the the actual
    # value is outside of what we expect.
    if kwargs.get('choices'):
        validate_normalized(obj, validate_choice_list, kwargs.get('choices'))

    # If a pattern was specified, then we will want to pull the pattern from
    # the pattern map and validate that the
    if kwargs.get('pattern') and kwargs.get('pattern') in pmap.keys():
        validate_normalized(obj, validate_regex_pattern, pmap[kwargs.get('pattern')])

    # If there wasn't a pattern matching that identifier, then throw an
    # IndexError
    elif kwargs.get('pattern') and kwargs.get('pattern') not in pmap.keys():
        raise IndexError('pattern name {} not found in map'.format(pattern))

    # If a raw regex pattern was provided instead, then we will pass that over
    # and validate
    elif kwargs.get('regex'):
        validate_normalized(obj, validate_regex_pattern, kwargs.get('regex'))

    # if we made it this gauntlet without an exception being raised, then
    # assume everything is good to go and return the object passed to us
    # initially.
    return obj