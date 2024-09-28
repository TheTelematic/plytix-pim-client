import os
import platform
import sys

from plytix_pim_client.constants import (
    DEFAULT_AUTH_BASE_URL,
    DEFAULT_HTTP_RETRIES,
    DEFAULT_HTTP_TIMEOUT,
    DEFAULT_PIM_BASE_URL,
)
from plytix_pim_client.version import __version__

PLYTIX_API_KEY = os.getenv("PLYTIX_API_KEY")
PLYTIX_API_PASSWORD = os.getenv("PLYTIX_API_PASSWORD")
PLYTIX_PIM_BASE_URL = os.getenv("PLYTIX_PIM_BASE_URL", DEFAULT_PIM_BASE_URL)
PLYTIX_AUTH_BASE_URL = os.getenv("PLYTIX_AUTH_BASE_URL", DEFAULT_AUTH_BASE_URL)

HTTP_RETRIES = int(os.getenv("PLYTIX_HTTP_RETRIES", DEFAULT_HTTP_RETRIES))
HTTP_TIMEOUT = int(os.getenv("PLYTIX_HTTP_TIMEOUT", DEFAULT_HTTP_TIMEOUT))

USER_AGENT = f"plytix-pim-client/{__version__} Python/{sys.version} {platform.platform()}"
