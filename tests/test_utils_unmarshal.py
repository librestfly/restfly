import pytest
from httpx import Response
from pydantic import BaseModel
from pydantic_xml import BaseXmlModel
from restfly._utils import unmarshal


@pytest.fixture
def json_model() -> type[BaseModel]:
    class Test(BaseModel):
        a: int

    return Test


@pytest.fixture
def xml_model() -> type[BaseXmlModel]:
    class Test(BaseXmlModel):
        a: int

    return Test


@pytest.fixture
def json_error_model() -> type[BaseModel]:
    class TestError(BaseModel):
        value: str

    return TestError


@pytest.fixture
def xml_resp() -> Response:
    return Response(status_code=200, content=b"<Test>2</Test>")


@pytest.fixture
def json_resp() -> Response:
    return Response(status_code=200, content=b'{"a": 1}')


@pytest.fixture
def json_list_resp() -> Response:
    return Response(status_code=200, content=b'[{"a": 1}, {"a": 2}]')


@pytest.fixture
def json_error_resp() -> Response:
    return Response(status_code=400, content=b'{"value": "error"}')


def test_unmarshal_pydantic(json_resp, json_model):
    resp = unmarshal(json_resp, model=json_model)
    assert resp == json_model(a=1)


def test_unmarshal_pydantic_xml(xml_resp, xml_model):
    resp = unmarshal(xml_resp, model=xml_model)
    assert resp == xml_model(a=2)


def test_unmarshal_pydantic_typeadapter(json_list_resp, json_model):
    resp = unmarshal(json_list_resp, model=list[json_model])
    assert resp == [json_model(a=1), json_model(a=2)]


def test_unmarshal_typeerror(json_resp):
    with pytest.raises(TypeError):
        unmarshal(json_resp, model=dict[str, str])
