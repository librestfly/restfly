from typing import Any, Dict

from restfly.errors import RestflyException, UnauthorizedError
from restfly.iterator import APIIterator


class GithubIterator(APIIterator):
    """
    Github Iterator class

    This class is used to iterate over Github API paginated resources. It
    overrides the `_get_page` method to handle the pagination parameters
    specific to the Github API.

    Github User API uses the user id as an offset. User with id greater than the
    `since` parameter will be returned. For each page, a maximum of 100 users
    can be returned. This can be set using the per_page parameter.

    This iterator will automatically handle this pagination scheme by
    updating the `since` parameter after each page is retrieved.

    Attributes:
        _path (str): The path to the resource.
        _params (Dict[str, Any]): The query parameters to be passed to the API.
            per_page (int): The number of items to be returned per page.
            since (int): A user ID. Only return users with an ID greater than this ID.
        max_pages: The maximum number of pages to return before stopping the iteration
        max_items: The maximum number of users to return before stopping the iteration

    Docs: https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#list-users
    """

    _path: str
    _params: Dict[str, Any] = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._log.debug(f'max_pages: {self.max_pages} | max_items: {self.max_items}')

    def _get_page(self):
        """
        Retrieves a page of data from the API.

        This method handles the Github API pagination.
        Based on the number of records fethced, the offset is updated.
        """
        self._log.debug(f'num_pages: {self.num_pages}, count: {self.count}')
        try:
            resp = self._api.get(self._path, params=self._params)

            # If users are returned, update the `since` to last user id
            if resp.ok:
                resp = resp.json()
                self._params['since'] = resp[-1]['id']
            else:
                resp.raise_for_status()

            # Updating the page of data with new users
            # Not updating self.total as Github API does not provide total user count
            self.page = resp
        except UnauthorizedError as login_error:
            self._log.error(f'Authentication failure. Error Details: {login_error}')
        except RestflyException as ex:
            self._log.error(f'Error fetching page: {ex}')
