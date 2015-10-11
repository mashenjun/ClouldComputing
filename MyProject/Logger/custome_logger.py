__author__ = 'mashenjun'
import logging, sys


def get_logger(name):
    logger = logging.getLogger(__name__)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    logger_handler.setLevel(logging.DEBUG)
    logger.addHandler(logger_handler)
    logger.setLevel(logging.DEBUG)
    return logger
