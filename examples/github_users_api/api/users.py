import logging

from restfly.endpoint import APIEndpoint
from restfly.errors import RestflyException, UnauthorizedError

from .iterator import GithubIterator


class UsersAPI(APIEndpoint):
    """
    Allows the users to get the list of Github users. It also has
    support to get the details of the current authenticated user.
    """

    _path = 'users'
    log = logging.getLogger('GithubLogger')

    def list(
        self,
        per_page: int = 10,
        since: int = 0,
        max_pages: int = 5,
        max_items: int = 50,
    ) -> GithubIterator:
        """
        List 50 users by default. Update the parameters as per requirement.

        Args:
            per_page (int): The maximum number of users to return per page.
            since (int): The offset to start from.
            max_pages (int): The maximum number of pages to request.
            max_items (int): The maximum number of items to request.

        Returns:
            GithubIterator: An iterator for the Github users.
        """
        # Maximum page length allowed by github for user API is 100
        if per_page > 100:
            per_page = 100
        params = {'per_page': per_page, 'since': since}

        return GithubIterator(
            self._api,
            _path=self._path,
            _params=params,
            max_pages=max_pages,
            max_items=max_items,
        )

    def get_current_user(self):
        """
        Retrieves the current authenticated user.

        Docs: https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#get-the-authenticated-user

        Returns:
            dict: A dictionary containing the details of the current user.
        """
        try:
            resp = self._api.get('user')
            if resp.ok:
                return resp.json()
            resp.raise_for_status()
        except UnauthorizedError as login_error:
            self.log.error(f'Authentication failure. Error Details: {login_error}')
        except RestflyException as ex:
            self.log.error(f'Error fetching current user: {ex}')
