__author__ = 'mashenjun'
import logging, sys, os
import threading
import time

pirpath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
path_to_log = os.path.join(pirpath,"Logger","main.log")
path_to_static_log = os.path.join(pirpath,"Logger","static.log")
path_to_metrix_log = os.path.join(pirpath,"Logger","allocate.log")
path_to_startTotalTime_log = os.path.join(pirpath,"Logger","startTotalTime.log")
path_to_launch_new_instance_time_log = os.path.join(pirpath,"Logger","launch_new_instance_time.log")
path_to_process_image_time_log = os.path.join(pirpath,"Logger","process_image_time.log")
path_to_worker_life_time_log = os.path.join(pirpath,"Logger","worker_life_time.log")
path_to_total_time_log = os.path.join(pirpath,"Logger","total_time.log")
path_to_trace_worker_wall_time_log = os.path.join(pirpath,"Logger","trace_worker_wall_time.log")
path_to_elasic_log = os.path.join(pirpath,"Logger","elastic_resource_scaling.log")
path_to_worker_log = os.path.join(pirpath,"Logger","worker_duty_cycle.log")
path_to_allocate_interval_log = os.path.join(pirpath,"Logger","allocate_interval.log")
path_to_busy_workers_log = os.path.join(pirpath,"Logger","busy_workers.log")

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

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

def get_allocate_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_metrix_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_metrix_startTotalTime_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_startTotalTime_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_launch_new_instance_time_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_launch_new_instance_time_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_process_image_time_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_process_image_time_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_worker_life_time_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_worker_life_time_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_total_time_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_total_time_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger


def get_trace_worker_wall_time_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_trace_worker_wall_time_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_elastic_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_elasic_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_worker_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_worker_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_allocate_interval_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_allocate_interval_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def get_busy_workers_logger(name):
    logger = logging.getLogger(name)
    logger_handler = logging.StreamHandler(stream=sys.stdout)
    hdlr = logging.FileHandler(path_to_busy_workers_log)
    formatter = logging.Formatter('%(message)s')
    logger_handler.setLevel(logging.DEBUG)
    logger_handler.setFormatter(formatter)
    hdlr.setFormatter(formatter)
    logger.addHandler(logger_handler)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

def record_busy_workers(static):
    bwlogger = get_busy_workers_logger("busy worker")
    while 1:
        bwlogger.debug(str(time.time()) + " : " + str(len(static.get_busy())))
        time.sleep(2)

def start_record_busy_workers(static):
    thread(record_busy_workers , static)