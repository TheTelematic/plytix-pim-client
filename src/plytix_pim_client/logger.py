import logging
import os
import sys

logger = logging.Logger("plytix_pim_client")
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False
