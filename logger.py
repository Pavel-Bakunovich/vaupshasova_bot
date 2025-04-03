import logging
#template_info = "{time}: {message}"
#template_error = "{time}: ERROR: {message}"
#date_format="%d %b %Y %H:%M:%S"
logger = logging.getLogger(__name__)
#consoleHandler = logging.StreamHandler()
#consoleHandler.setFormatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
#logger.addHandler(consoleHandler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def log(message):
    logger.info(message)

def log_error(error_message):
    logger.error(error_message)
