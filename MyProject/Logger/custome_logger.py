__author__ = 'mashenjun'
import logging, sys


def get_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.setLevel(logging.DEBUG)
    return logger
