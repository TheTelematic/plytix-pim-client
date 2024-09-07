import logging
import os
import sys

logger = logging.getLogger(__package__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))

if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

logger.propagate = False
