import logging
import os

logger = logging.Logger(__package__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
handler = logging.StreamHandler()
handler.setLevel(os.getenv("LOG_LEVEL", logging.INFO))
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False
