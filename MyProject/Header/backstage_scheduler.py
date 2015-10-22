# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 14:14:04 2015

@author: yun
"""

import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from os.path import join
from S3 import handler as S3_handler
from SQS import handler as SQS_handler
from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
from dirtools import Dir, DirState
from static import static as static_handler
import threading
import time
import scheduler
import math

logger = custome_logger.get_logger(__file__)
config = Config()
valid = 1

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def check_the_idle_list(sqs):
    global valid
    while (valid):
        # get both the idle instances number and the waiting tasks
        idle_num = len(static_handler.get_idle())
        if (idle_num>0) :
            scheduler.send_message_to_sqs(sqs)       
            
def launch_new_instances(ec2):
    global valid
    while (valid):
       # compare the idle instances with the local queue
        idle_num = len(static_handler.get_idle())
        waiting_tasks = len(scheduler.LOCAL_QUEUE)
        extra_workers = math.ceil(waiting_tasks - idle_num)/2
        if (extra_workers>0) :
            EC2_handler.create_instance_from_image(ec2,extra_workers)
        
            
        
def start_backstage_scheduler(sqs,ec2):
    #start the thread
    thread(check_the_idle_list,sqs)
    thread(launch_new_instances,ec2)
