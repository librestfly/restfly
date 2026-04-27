"""
RESTFly Library Package
"""

from ._async import AsyncAPIClient, AsyncAPIEndpoint
from ._errors import APIError, ErrorStatus, RetryError
from ._iterator import APIIterator, AsyncAPIIterator
from ._sync import APIClient, APIEndpoint
from ._version import version as __version__

__author__ = "Steven McGrath <steve@mcgrath.sh>"
__all__ = [
    "AsyncAPIClient",
    "AsyncAPIEndpoint",
    "AsyncAPIIterator",
    "APIClient",
    "APIEndpoint",
    "APIIterator",
    "APIError",
    "ErrorStatus",
    "RetryError",
    "__version__",
]
