from typing import Any, get_origin, get_type_hints, overload

from httpx import Response
from pydantic import BaseModel, TypeAdapter
from pydantic_xml import BaseXmlModel

from ._types import Model, XMLModel


@overload
def unmarshal(
    response: Response,
    *,
    model: type[XMLModel],
    json_model_kwargs: dict[str, Any] | None = ...,
    xml_model_kwargs: dict[str, Any] | None = ...,
) -> XMLModel: ...


@overload
def unmarshal(
    response: Response,
    *,
    model: type[Model],
    json_model_kwargs: dict[str, Any] | None = ...,
    xml_model_kwargs: dict[str, Any] | None = ...,
) -> Model: ...


@overload
def unmarshal(
    response: Response,
    *,
    model: type[list[Model]],
    json_model_kwargs: dict[str, Any] | None = ...,
    xml_model_kwargs: dict[str, Any] | None = ...,
) -> list[Model]: ...


def unmarshal(
    response: Response,
    *,
    model: type[Model] | type[XMLModel] | type[list[Model]],
    json_model_kwargs: dict[str, Any] | None = None,
    xml_model_kwargs: dict[str, Any] | None = None,
) -> XMLModel | Model | list[Model]:
    # initialize the mutables.
    json_model_kwargs = {} if json_model_kwargs is None else json_model_kwargs
    xml_model_kwargs = {} if xml_model_kwargs is None else xml_model_kwargs
    # If the model has an origin or list, then we will need to wrap it in a type
    # adapter and return the model that way.  This allows us to handle things like
    # lists just like how FastAPI allows you to wrap models in list definitions.
    #
    # NOTE: We could likely expand the type adapter to support more use cases, but
    #       are purposefully keeping this constrained here.
    if get_origin(model) is list:
        return TypeAdapter(model).validate_json(response.content, **json_model_kwargs)

    # As Pydantic-XML base-classes the Pydantic BaseModel, we will first check to see
    # if the model passed to us is a Pydantic-XML model.  If it is, then unmarshal the
    # XML data.
    elif isinstance(model, type) and issubclass(model, BaseXmlModel):
        return model.from_xml(response.content, **xml_model_kwargs)

    # If the model is a Pydantic class, then unmarshal with validate_json.
    elif isinstance(model, type) and issubclass(model, BaseModel):
        return model.model_validate_json(response.content, **json_model_kwargs)

    # As None of the valid types were discovered, raise a type error and inform the
    # caller that we don't know how to process what was passed.
    raise TypeError(f"model {model} is not a valid type.")


def assign_annotations(obj: Any, base_type: type[Any]) -> None:
    """
    Assigns public attributes that have an annotation of the base_type.
    """
    annotations = get_type_hints(obj.__class__)
    # For each annotation, we want to check to see if the attribute name is prefixed
    # with an underscore (which would denote that it is private) and to check to see
    # if it is of the base type.  If both are true, then we will instantiate the
    # annotated public attribute with the annotated type, passing the Any as the
    # only attribute.
    for attr, obj_type in annotations.items():
        if (
            attr[0] != "_"
            and isinstance(obj_type, type)
            and issubclass(obj_type, base_type)
        ):
            setattr(obj, attr, obj_type(obj))
