__author__ = 'mashenjun'
import logging, sys, os

pirpath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
path_to_log = os.path.join(pirpath,"Logger","main.log")
path_to_static_log = os.path.join(pirpath,"Logger","static.log")

def get_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_log)
    formatter = logging.Formatter('%(name)s - %(asctime)s - %(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_static_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_static_log)
    formatter = logging.Formatter('%(name)s - %(asctime)s - %(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger
