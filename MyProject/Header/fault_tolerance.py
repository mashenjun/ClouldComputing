
__author__ = 'yunlu'

import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
from Logger.custome_logger import get_logger
from SQS import handler as SQS_handler
from EC2 import cmdshell as ec2cmdshell

import threading
import time
import scheduler

logger = get_logger(__file__)
config = Config()
valid = 1
INPUT_QUEUE = config.ConfigSectionMap()["sqs_input_queue"]

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def check_survive(ec2,static):
    # busy list from static
    to_check_list_busy = static.get_busy()
    to_check_list_idle = static.get_idle()
    #for check_id in to_check_list:
        #instance_status_list = EC2_handler.get_instance_status(ec2,check_id)
        #instance_status = instance_status_list [0]['InstanceState']['Name']
    # get now working instance list
    compared_instance_list = EC2_handler.get_instance_running_worker(ec2)
    compared_instance_ID = EC2_handler.get_instanceId(compared_instance_list)
    logger.debug("the compared_instance_id is "+str(compared_instance_ID)+" with busy "+str(to_check_list_busy) +" and idle "+str(to_check_list_idle))
    # compare these lists, the result is the fault instances list
    not_match_busy = [x for x in to_check_list_busy if x not in compared_instance_ID]
    not_match_idle = [x for x in to_check_list_idle if x not in compared_instance_ID]
    return not_match_busy,not_match_idle

def reboot_not_match(ec2,client,static,sqs):
    global valid
    while (valid):
        not_match_busy,not_match_idle = check_survive(ec2,static)
        #logger.debug("reboot_id_list (original busy)"+ str(reboot_id_list))
        #EC2_handler.start_instance(reboot_id_list)
        if len(not_match_busy) > 0:
            logger.debug("reboot_id_list (original busy)"+ str(not_match_busy))
            static.remove_from_busy(not_match_busy)
            for instance_id in not_match_busy:
                logger.debug("Reboot del register in details")
                last_job = static.de_register_in_details(instance_id)
                if (not last_job == None):
                    header_IP = EC2_handler.get_local_ipv4()
                    headloaction = header_IP +":9999"
                    # bind the job with local ip
                    msg= last_job + "#" +headloaction
                    # put the job into the input queue again
                    # SQS_handler.create_msg(sqs, INPUT_QUEUE, msg)
                    # put the job into the local queue
                    logger.debug("Reboot busy instance add msg, which is")
                    scheduler.insert_new_job([last_job],static,0)
                    logger.debug("Reboot busy instance add msg, which is" + str(last_job) + "in static, now static is:" + str(scheduler.LOCAL_QUEUE))
                thread(start_stopping_instance_idle,ec2,client,instance_id)

        elif len(not_match_idle) > 0:
            logger.debug("reboot_id_list (original idle)"+ str(not_match_idle))
            for instance_id in not_match_idle:
                static.move_from_idle_to_pending(instance_id)
                thread(start_stopping_instance_idle,ec2,client,instance_id)
        time.sleep(2)
    #return response

"""
def check_survive_idle(ec2,static):
    # busy list from static
    to_check_list = static.get_idle()
    compared_instance_list = EC2_handler.get_instance_running_worker(ec2)
    compared_instance_ID = EC2_handler.get_instanceId(compared_instance_list)
    # compare these lists, the result is the fault instances list
    not_match = [x for x in to_check_list if x not in compared_instance_ID]
    return not_match

def reboot_not_match_idle(ec2,client,static,sqs):
    global valid
    while (valid):
        reboot_id_list = check_survive_idle(ec2,static)
        for instance_id in reboot_id_list:
            static.move_from_idle_to_pending(instance_id)
            thread(start_stopping_instance_idle,ec2,client,instance_id)
    time.sleep(5)


def start_stopping_instance(ec2,client,reboot_id,static):
    while (1):
        time.sleep(1)
        logger.debug("the stopped worker are" + str(EC2_handler.get_stopped_worker(ec2)))
        if reboot_id in EC2_handler.get_stopped_worker(ec2):
            logger.debug("stopped_worker are" + str(EC2_handler.get_stopped_worker(ec2)) + "to check the id" + str(reboot_id))
            break
    EC2_handler.start_instance(client, reboot_id)
    while(not EC2_handler.get_instance_status(ec2,reboot_id)):
        time.sleep(2)
    ec2cmdshell.get_instance(reboot_id)
    scheduler.ssh_the_worker(reboot_id)
    static.add_to_busy(reboot_id)
"""

def start_stopping_instance_idle(ec2,client,reboot_id):
    while (1):
        time.sleep(1)
        stopped_instances = EC2_handler.get_stopped_worker(ec2)
        stopped_instances_ids = EC2_handler.get_instanceId(stopped_instances)
        logger.debug("the stopped worker are" + str(stopped_instances_ids))
        if reboot_id in stopped_instances_ids:
            break
    EC2_handler.start_instance(client,reboot_id)


def start_check_survive(ec2,client,static,sqs):
    #start the thread
    thread(reboot_not_match,ec2,client,static,sqs)
    #thread(reboot_not_match_idle,ec2,client,static,sqs)



