from restfly._errors import APIError, ErrorStatus, build_error_map


def test_build_error_map_defaults():
    error_map = build_error_map()
    assert error_map[400] == ErrorStatus(
        template=r"[400] Bad Request {request.method} {request.url}"
    )
    assert error_map[699] == ErrorStatus()


def test_build_error_map_overloads():
    error_map = build_error_map(overloads={401: ErrorStatus(template="I'm a message")})
    assert error_map[401] == ErrorStatus(template="I'm a message")
    assert error_map[400] == ErrorStatus(
        template=r"[400] Bad Request {request.method} {request.url}"
    )
    assert error_map[699] == ErrorStatus()


def test_build_error_map_api_error_class_overload():
    class ExampleError(APIError): ...

    error_map = build_error_map(error_class=ExampleError)
    assert error_map[400] == ErrorStatus(
        exception=ExampleError,
        template=r"[400] Bad Request {request.method} {request.url}",
    )
    assert error_map[699] == ErrorStatus(exception=ExampleError)
