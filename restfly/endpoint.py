'''
Endpoints
=========

.. autoclass:: APIEndpoint
    :members:
    :private-members:
'''
from .utils import force_case
from .errors import UnexpectedValueError
import re


class APIEndpoint(object):
    '''
    APIEndpoint is the base model for which all API endpoint classes are
    sired from.  The main benefit is the addition of the ``_check()``
    function from which it's possible to check the type & content of a
    variable to ensure that we are passing good data to the API.

    Attributes:
        _pattern_map (dict):
            A definition of regex patterns that can be used with the
            :obj:`_check` method.  These are used with the ``pattern`` argument.
        _custom_pattern_map (dict):
            A dictionary of custom regex pattern definitions, same as the
            :obj:`_pattern_map` attribute.  As overloading this one will not
            replace the default patterns, this one is considered additive.
            The custom mapping is checked **after** the default patterns.

    Args:
        api (APISession):
            The APISession (or sired child) instance that the endpoint will
            be using to perform calls to the API.
    '''
    _pattern_map = {
        'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        'hex': r'^[a-fA-f0-9]+$',
        'url': r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',
        'ipv4': r'^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$',
        'ipv6': r'^s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:)))(%.+)?s*(\/([0-9]|[1-9][0-9]|1[0-1][0-9]|12[0-8]))?$',
    }
    _custom_pattern_map = dict()

    def __init__(self, api):
        self._api = api
        self._log = api._log


    def _check(self, name, obj, expected_type, choices=None, default=None,
               case=None, pattern=None, regex=None, items_type=None):
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
                Specify a regex pattern from the pattern map variable.
            regex (str, optional):
                Validate that the value of the object matches this pattern.
            items_type (type, optional):
                If the expected type is an iterable, and if all of the items
                within that iterable are expected to be a given type, then
                specifying the type here will enable checking each item within
                the iterable.  NOTE: this will traverse the iterable.

        Returns:
            :obj:`Object`:
                Either the object or the default object depending.

        Examples:
            Ensure that the value is an integer type:

            >>> self._check('example', val, int)

            Ensure that the value of val is within 0 and 100:

            >>> self._check('example', val, int, choices=list(range(100)))
        '''
        def validate_regex_pattern(regex, obj):
            if len(re.findall(regex, str(obj))) <= 0:
                raise UnexpectedValueError(
                    '{} has value of {}.  Does not match pattern {}'.format(
                        name, obj, pattern))

        def validate_choice_list(choices, obj):
            if obj not in choices:
                raise UnexpectedValueError(
                    '{} has value of {}.  Expected one of {}'.format(
                        name, obj, ','.join([str(i) for i in choices])))

        def validate_expected_type(expected, obj):
            if not isinstance(obj, expected):
                raise TypeError('{} is of type {}.  Expected {}.'.format(
                name,
                obj.__class__.__name__,
                expected_type.__name__
                    if hasattr(expected_type, '__name__') else expected_type
            ))


        # We have a simple function to convert the case of string values so that
        # we can ensure correct output.

        # Convert the case of the inputs.
        obj = force_case(obj, case)
        choices = force_case(choices, case)
        default = force_case(default, case)

        # If the object sent to us has a None value, then we will return None.
        # If a default was set, then we will return the default value.
        if obj == None:
            return default

        # If we are checking for a string type, we will also want to check for
        # unicode type transparently, so add the unicode type to the expected
        # types list.  NOTE this is for Python2 only, as Python3 treats all
        # strings as type string.
        if expected_type == str:
            try:
                expected_type = (str, unicode)
            except NameError:
                pass

        # If the object is none of the right types then we want to raise a
        # TypeError as it was something we weren't expecting.
        validate_expected_type(expected_type, obj)

        if items_type:
            # If the items within the list should also be of a specific type,
            # we can check those as well
            for item in obj:
                validate_expected_type(items_type, item)

        # if the object is only expected to have one of a finite set of values,
        # we should check against that and raise an exception if the the actual
        # value is outside of what we expect.
        if choices:
            if isinstance(obj, (list, tuple)):
                # If the object is a list or tuple type, then lets ensure that
                # all of the items within the obj .
                for item in obj:
                    validate_choice_list(choices, item)
            else:
                validate_choice_list(choices, obj)

        # If a pattern was specified, then we will want to pull the pattern from
        # the pattern map and validate that the
        if pattern and pattern in self._pattern_map:
            # If we have a pattern from the pattern map, then validate with that
            # pattern.
            if isinstance(obj, (list, tuple)):
                for item in obj:
                    validate_regex_pattern(self._pattern_map[pattern], item)
            else:
                validate_regex_pattern(self._pattern_map[pattern], obj)
        elif pattern and pattern in self._custom_pattern_map:
            # If we have a pattern from the user-defined pattern map, then
            # validate with that pattern.
            if isinstance(obj, (list, tuple)):
                for item in obj:
                    validate_regex_pattern(
                        self._custom_pattern_map[pattern], item)
            else:
                validate_regex_pattern(self._custom_pattern_map[pattern], obj)
        elif (pattern and (pattern not in self._pattern_map
          or pattern not in self._custom_pattern_map)):
            # If there wasn't a pattern matching that identifier, then throw an
            # IndexError
            raise IndexError('pattern name {} not found in map'.format(pattern))
        elif regex:
            # If a raw regex pattern was provided instead, then we will pass
            # that over and validate
            if isinstance(obj, (list, tuple)):
                for item in obj:
                    validate_regex_pattern(regex, item)
            else:
                validate_regex_pattern(regex, obj)

        # if we made it this gauntlet without an exception being raised, then
        # assume everything is good to go and return the object passed to us
        # initially.
        return obj