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

    def __init__(
        self, url: str = 'https://api.github.com', token: str | None = None, **kwargs
    ):
        """
        Initialize the Github API Session.
        """
        if not token:
            token = os.getenv('GITHUB_TOKEN')
        if not token:
            raise ConnectionError('No Github token has been provided')

        if 'token' not in kwargs.keys():
            kwargs.setdefault('token', token)

        if 'url' not in kwargs.keys():
            kwargs.setdefault('url', url)

        super().__init__(**kwargs)

    def _authenticate(self, token: str):
        self._session.headers = {'Authorization': f'Bearer {token}'}

    def _deauthenticate(self):
        self._session.headers = {'Authorization': None}

    @property
    def users(self):
        return UsersAPI(self)
