import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOG_LEVEL = 10
LOG_FILE = '/path/to/file.log'
LOG_FILE_SIZE = 1024


class ServiceLogger:
    def __init__(self, name):
        # Create a logger for services
        logger = logging.getLogger(name)
        logger.setLevel(LOG_LEVEL)

        # Append current date time and log level to the beginning of the log message
        formatter = logging.Formatter(
            '%(asctime)s %(name)s %(levelname)-5s %(message)s'
        )

        if os.getenv('ENVIRONMENT') == 'production':
            # When the log file size reaches a certain limit, create a new file
            handler = RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=LOG_FILE_SIZE,
            )
        else:
            handler = logging.StreamHandler(stream=sys.stdout)

        handler.setFormatter(formatter)

        if not logger.hasHandlers():
            logger.addHandler(handler)
        logger.propagate = False

        self.logger = logger

    def info(self, **kwargs):
        return self.log(level=logging.INFO, **kwargs)

    def debug(self, **kwargs):
        return self.log(level=logging.DEBUG, **kwargs)

    def warning(self, **kwargs):
        return self.log(level=logging.WARNING, **kwargs)

    def error(self, **kwargs):
        return self.log(level=logging.ERROR, **kwargs)

    def exception(self, **kwargs):
        # Only be used when there's an exception
        return self.log(level=logging.CRITICAL, **kwargs)

    def log(self, level, message, data=None):
        msg = f'| {message} | {json.dumps(data, default=str)} |'

        if level == logging.CRITICAL:
            self.logger.exception(msg)
        else:
            self.logger.log(level, msg)

        return msg
