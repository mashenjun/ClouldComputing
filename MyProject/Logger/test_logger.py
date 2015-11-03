__author__ = 'yun'

import custome_logger as cl
import time
import threading

logger = cl.get_logger("Hello")
mlogger = cl.get_allocate_logger("World")


class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()


def output_to_logger ():
    while 1:
        logger.debug("I am in logger~~~")
    time.sleep(0.5)

def output_to_mlogger ():
    while 1:
        mlogger.debug("I am in mlogger~~~")
    time.sleep(1)

def start_backstage_scheduler():
    #start the thread
    thread(output_to_logger)
    thread(output_to_mlogger)

if __name__ == "__main__":
    start_backstage_scheduler()