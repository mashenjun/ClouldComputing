__author__ = 'yunlu'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from os.path import join
from S3 import handler as S3_handler
from SQS import handler as SQS_handler
from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
from Logger.custome_logger import get_logger

import threading
import time
import scheduler
import math

logger = get_logger(__file__)
config = Config()
valid = 1
count = 0

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def delete_worker(ec2,static):
    global count
    global valid
    while (valid):
        idle_num = static.get_idle_num()
        if idle_num >= 3:
            count+=1
        elif idle_num < 2:
            count-=1

        if count > 3 & idle_num > 3:
            instanceid = static.get_idle()[-1]
            EC2_handler.terminate_instance(ec2,instanceid)
            count = 0

        time.sleep(3)


def start_delete_worker(ec2,static):
    #start the thread
    thread(delete_worker,ec2,static)






