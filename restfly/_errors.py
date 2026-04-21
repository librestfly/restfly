import logging
from dataclasses import dataclass

from httpx import Response
from pydantic import BaseModel


class RetryError(Exception):
    def __init__(self, url: str, method: str, attempts: int):
        super().__init__(f"Too many attempts ({attempts}) to {method} {url}")


class APIError(Exception):
    status_code: int
    """ Status code of the HTTP Response """

    response: Response
    """ HTTPX Response object of the exception """

    obj: BaseModel | None
    """ Coerced data obj of the response (if any) """

    def __init__(
        self,
        response: Response,
        template: str,
        obj: BaseModel | None = None,
    ):
        self.status_code = response.status_code
        self.obj = obj
        self.response = response
        msg = template.format(response=response, request=response.request)
        logger = logging.getLogger(__name__)
        logger.warning(msg)
        super().__init__(msg)


@dataclass
class ErrorStatus:
    retry: bool = False
    template: str = (
        r"[{response.status_code}] Response from {request.method} {request.url}"
    )
    model: type[BaseModel] | None = None
    exception: type[APIError] = APIError
    backoff: float = 1.0
    jitter: float = 0.5


def default_error_status() -> ErrorStatus:
    return ErrorStatus()


ERROR_MAP = {
    400: ErrorStatus(template=r"[400] Bad Request {request.method} {request.url}"),
    401: ErrorStatus(template=r"[401] Unauthorized {request.method} {request.url}"),
    402: ErrorStatus(template=r"[402] Payment Required {request.method} {request.url}"),
    403: ErrorStatus(template=r"[403] Access Forbidden {request.method} {request.url}"),
    404: ErrorStatus(template=r"[404] Not Found {request.method} {request.url}"),
    405: ErrorStatus(
        template=r"[405] Method Not Allowed {request.method} {request.url}"
    ),
    406: ErrorStatus(template=r"[406] Not Acceptable {request.method} {request.url}"),
    407: ErrorStatus(
        template=r"[407] Proxy Auth Required {request.method} {request.url}"
    ),
    408: ErrorStatus(
        template=r"[408] Request Timed Out {request.method} {request.url}"
    ),
    409: ErrorStatus(template=r"[409] Request Conflict {request.method} {request.url}"),
    410: ErrorStatus(template=r"[410] Gone {request.method} {request.url}"),
    411: ErrorStatus(template=r"[411] Length Required {request.method} {request.url}"),
    412: ErrorStatus(
        template=r"[412] Precondition Failed {request.method} {request.url}"
    ),
    413: ErrorStatus(
        template=r"[413] Content Too Large {request.method} {request.url}"
    ),
    414: ErrorStatus(template=r"[414] URI Too Long {request.method} {request.url}"),
    415: ErrorStatus(
        template=r"[415] Unsupported Media Type {request.method} {request.url}"
    ),
    416: ErrorStatus(
        template=r"[416] Range Not Satisfiable {request.method} {request.url}"
    ),
    417: ErrorStatus(
        template=r"[417] Expectation Failed {request.method} {request.url}"
    ),
    418: ErrorStatus(template=r"[418] I'm a Teapot {request.method} {request.url}"),
    421: ErrorStatus(
        template=r"[421] Misdirected Request {request.method} {request.url}"
    ),
    422: ErrorStatus(
        template=r"[422] Unprocessable Content {request.method} {request.url}"
    ),
    423: ErrorStatus(template=r"[423] Locked {request.method} {request.url}"),
    424: ErrorStatus(
        template=r"[424] Failed Dependency {request.method} {request.url}"
    ),
    425: ErrorStatus(template=r"[425] Too Early {request.method} {request.url}"),
    426: ErrorStatus(template=r"[426] Upgrade Required {request.method} {request.url}"),
    428: ErrorStatus(
        template=r"[428] Precondition Required {request.method} {request.url}"
    ),
    429: ErrorStatus(
        retry=True,
        template=r"[429] Too Many Requests to {request.method} {request.url}",
        backoff=30,
    ),
    431: ErrorStatus(
        template=r"[431] Request Header Fields Too Large {request.method} {request.url}"
    ),
    451: ErrorStatus(
        template=r"[451] Unavailable For Legal Reasons {request.method} {request.url}"
    ),
    500: ErrorStatus(
        template=r"[500] Internal Server Error {request.method} {request.url}"
    ),
    501: ErrorStatus(template=r"[501] Not Implemented {request.method} {request.url}"),
    502: ErrorStatus(
        retry=True,
        template=r"[502] Bad Gateway Response {request.method} {request.url}",
        backoff=10,
    ),
    503: ErrorStatus(
        retry=True,
        template=r"[503] Service Unavailable {request.method} {request.url}",
        backoff=10,
    ),
    504: ErrorStatus(
        retry=True,
        template=r"[504] Gateway Timeout {request.method} {request.url}",
        backoff=10,
    ),
    505: ErrorStatus(
        template=r"[505] HTTP Version Not Supported {request.method} {request.url}"
    ),
    506: ErrorStatus(
        template=r"[506] Variant Also Negotiates {request.method} {request.url}"
    ),
    507: ErrorStatus(
        template=r"[507] Insufficient Storage {request.method} {request.url}"
    ),
    508: ErrorStatus(template=r"[508] Loop Detected {request.method} {request.url}"),
    510: ErrorStatus(template=r"[510] Not Extended {request.method} {request.url}"),
    511: ErrorStatus(
        template=r"[511] Network Authentication Required {request.method} {request.url}"
    ),
}
