import logging
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

class MinskFormatter(logging.Formatter):
    def converter(self, timestamp):
        return datetime.fromtimestamp(timestamp, tz=ZoneInfo("Europe/Minsk")).timetuple()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False

formatter = MinskFormatter("%(asctime)s [%(levelname)s] %(message)s")

if not logger.handlers:
    info_handler = logging.StreamHandler(sys.stdout)
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)

    error_handler = logging.StreamHandler(sys.stderr)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

def log(message):
    logger.info(message)

def log_error(error_message):
    logger.error(error_message)


