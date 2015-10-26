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
from Logger.custome_logger import get_logger

import threading
import time
import scheduler
import math

logger = get_logger(__file__)
config = Config()
valid = 1


class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def check_the_idle_list(sqs,static):
    global valid
    while (valid):
        # get both the idle instances number and the waiting tasks

        idle_num = len(static.get_idle())
        if (idle_num > 0) :
            scheduler.send_message_to_sqs(sqs,static)

def launch_new_instances(ec2,static):
    global valid
    while (valid):
        
       # compare the idle instances with the local queue
        idle_num = len(static.get_idle())
        count = static.get_sum()
        #waiting_tasks = len(scheduler.LOCAL_QUEUE)
        global LOCAL_QUEUE
        all_tasks = []        
        [all_tasks.extend(v['Tasks']) for k,v in scheduler.LOCAL_QUEUE.items()]
        waiting_tasks = len(all_tasks)
        extra_workers = math.ceil((waiting_tasks - idle_num)/2)
        if (extra_workers>0) :
            instances = EC2_handler.create_instance_from_image(ec2,int(extra_workers),static)
            logger.debug("create"+extra_workers+" new instance"+str(instances)+"with thread")
            instanceid = EC2_handler.get_instanceId(instances)
            for i in instanceid:
                count += 1
                EC2_handler.set_key_name(ec2,i,"Name","Worker"+str(count))
    logger.debug("OUT launch_new_instances FUNCTION")
        
            
        
def start_backstage_scheduler(sqs,ec2,static):
    #start the thread
    thread(check_the_idle_list,sqs,static)
    thread(launch_new_instances,ec2,static)
