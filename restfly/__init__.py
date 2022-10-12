'''
RESTfly package
'''
from .version import (                       # noqa: F401
    VERSION as __version__,
    AUTHOR as __author__,
    DESCRIPTION as __description__
)
from .session import APISession              # noqa: F401
from .endpoint import APIEndpoint            # noqa: F401
from .iterator import APIIterator            # noqa: F401
