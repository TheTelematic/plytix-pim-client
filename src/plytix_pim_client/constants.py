import platform
import sys

from plytix_pim_client.version import __version__

DEFAULT_PIM_BASE_URL = "https://pim.plytix.com"
DEFAULT_AUTH_BASE_URL = "https://auth.plytix.com"

DEFAULT_USER_AGENT = f"plytix-pim-client/{__version__} Python/{sys.version} {platform.platform()}"

DEFAULT_HTTP_RETRIES = 3
DEFAULT_HTTP_TIMEOUT = 30

DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = DEFAULT_PAGE_SIZE

DEFAULT_WAIT_SECONDS_AFTER_AUTH_TOO_MANY_REQUESTS = 60 * 15
