import logging
import logging.handlers
from datetime import datetime


def setup_logging(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.propagate = False

    if logger.hasHandlers():
        for handler in logger.handlers[:]:
            if isinstance(handler, (logging.FileHandler, logging.handlers.TimedRotatingFileHandler)):
                logger.removeHandler(handler)
                handler.close()

    log_filename = datetime.now().strftime("%Y-%m-%d")
    fmt = logging.Formatter('[ %(asctime)s ] %(levelname)s : %(message)s')

    file_handler = logging.handlers.TimedRotatingFileHandler(
        f'./data/log/{log_filename}.log', when="midnight", backupCount=10
    )
    file_handler.setFormatter(fmt)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
