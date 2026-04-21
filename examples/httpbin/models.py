from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field
from pydantic_xml import BaseXmlModel, attr, element


class HTTPBinResponse(BaseModel):
    args: dict[str, str]
    data: str | None = None
    files: dict[str, str] | None = None
    form: dict[str, str] | None = None
    headers: dict[str, str]
    json_data: dict[str, Any] | None = Field(None, alias="json")
    origin: str
    url: str


## Example Response model for the /json endpoint.
class JsonResponse(BaseModel):
    slideshow: Slideshow


class Slideshow(BaseModel):
    author: str
    date: str
    slides: list[Slides]
    title: str


class Slides(BaseModel):
    title: str
    type: str
    items: list[str] | None = None


## Example Response model for the /xml endpoint.


class XmlSlideshow(BaseXmlModel, tag="slideshow"):
    title: str = attr()
    date: str = attr()
    author: str = attr()
    slides: list[XmlSlide] = element(tag="slide", default=None)


class XmlSlide(BaseXmlModel, tag="slide"):
    title: str = element()
    items: list[str] = element(tag="item", default=None)


XmlSlide.model_rebuild()
XmlSlideshow.model_rebuild()
