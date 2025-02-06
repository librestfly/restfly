import logging
import os

from restfly.session import APISession

from .users import UsersAPI


class GithubAPI(APISession):
    """
    Github API wrapper

    Docs:
        https://developer.github.com/v3/

    Args:
        url: The github API url
        token: The user github token
    """

    _log = logging.getLogger('GithubLogger')

    def __init__(self, **kwargs):
        """
        Initialize the Github API Session.
        """
        params = (
            ('url', os.getenv('GITHUB_URL')),
            ('token', os.getenv('GITHUB_TOKEN')),
            ('log_level', os.getenv('LOG_LEVEL')),
        )
        for key, envval in params:
            if envval and not kwargs.get(key):
                kwargs[key] = envval
        if not kwargs.get('url'):
            raise ConnectionError('GITHUB_URL is not provided')
        if not kwargs.get('token'):
            raise ConnectionError('GITHUB_TOKEN is not provided')
        logging.basicConfig(
            level=kwargs.get('log_level', logging.INFO), format='%(message)s'
        )
        super().__init__(**kwargs)

    def _authenticate(self, **kwargs):
        self._session.headers = {'Authorization': f'Bearer {kwargs.get("token")}'}

    def _deauthenticate(self, **kwargs):
        self._session.headers = {'Authorization': None}

    @property
    def users(self):
        return UsersAPI(self)
