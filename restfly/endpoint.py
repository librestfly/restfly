'''
Endpoints
=========

.. autoclass:: APIEndpoint
    :members:
    :private-members:
'''


class APIEndpoint(object):
    '''
    APIEndpoint is the base model for which all API endpoint classes are
    sired from.  The main benefit is the addition of the ``_check()``
    function from which it's possible to check the type & content of a
    variable to ensure that we are passing good data to the API.

    Args:
        api (APISession):
            The APISession (or sired child) instance that the endpoint will
            be using to perform calls to the API.
    '''
    def __init__(self, api):
        self._api = api
        self._log = api._log