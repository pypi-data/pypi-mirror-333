import logging
import os


def configure_logging(logger_level: str = logging.INFO):
    """
    Configures logging functionality across Pneuma's modules.

    ## Args
    - **logger_level** (int): The minimum level of log messages to be shown.
    """
    LOGGER_LOCATION = os.path.join(os.getcwd(), ".pneuma")
    os.makedirs(LOGGER_LOCATION, exist_ok=True)
    logger = logging.getLogger()
    if logger.hasHandlers():
        logger.handlers.clear()

    logging.basicConfig(
        level=logger_level,
        format="%(asctime)s [%(name)s] [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(os.path.join(LOGGER_LOCATION, "pneuma.log")),
            logging.StreamHandler(),
        ],
    )
