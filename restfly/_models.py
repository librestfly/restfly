from typing import Any, Literal, Self

from pydantic import BaseModel

from ._async import AsyncAPIClient
from ._sync import APIClient


class APIModel(BaseModel):
    __api_path__: str
    """
    String representation of the path using `model` to act as a placeholder for any
    formatting that needs to occur from the model.
    """

    __api_client__: APIClient | AsyncAPIClient | None = None
    """ APIClient object that the model is associated to. """

    __api_save_method__: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "PUT"
    """ HTTP method associated with the "save/async_save" methods. """

    __api_save_request_model_kwargs__: dict[str, Any] | None = None
    """ Pydantic model_dump kwargs to associate to the save method. """

    __api_remove_method__: Literal["GET", "POST", "PUT", "PATCH", "DELETE"] = "DELETE"
    """ HTTP method associated to the "remove/async_remove" methods. """

    def model_post_init(self, context: Any) -> Any:
        if isinstance(context, dict):
            self.__api_client__ = context.get("restfly_client")

    def save(self) -> Self:
        """
        Saves (updates) the current state of the object back to the API.

        Returns:
            Updated copy of the object from the upstream API.
        """
        path = self.__api_path__.format(model=self)
        if not isinstance(self.__api_client__, APIClient):
            raise TypeError(
                f"Cannot perform synchronous save using {self.__api_client__}."
            )
        return self.__api_client__._request(
            method=self.__api_save_method__,
            path=path,
            json=self,
            request_model_kwargs=self.__api_save_request_model_kwargs__,
            response_model=self.__class__,
        )

    def remove(self) -> None:
        """
        Removes (deletes) the object from the API.
        """
        path = self.__api_path__.format(model=self)
        if not isinstance(self.__api_client__, APIClient):
            raise TypeError(
                f"Cannot perform synchronous save using {self.__api_client__}."
            )
        self.__api_client__._request(
            method=self.__api_remove_method__,
            path=path,
        )

    async def async_save(self) -> Self:
        """
        Saves (updates) the current state of the object back to the API.

        Returns:
            Updated copy of the object from the upstream API.
        """
        path = self.__api_path__.format(model=self)
        if not isinstance(self.__api_client__, AsyncAPIClient):
            raise TypeError(
                f"Cannot perform synchronous save using {self.__api_client__}."
            )
        return await self.__api_client__._request(
            method=self.__api_save_method__,
            path=path,
            json=self,
            request_model_kwargs=self.__api_save_request_model_kwargs__,
            response_model=self.__class__,
        )

    async def async_remove(self) -> None:
        """
        Removes (deletes) the object from the API.
        """
        path = self.__api_path__.format(model=self)
        if not isinstance(self.__api_client__, AsyncAPIClient):
            raise TypeError(
                f"Cannot perform synchronous save using {self.__api_client__}."
            )
        await self.__api_client__._request(
            method=self.__api_remove_method__,
            path=path,
        )
