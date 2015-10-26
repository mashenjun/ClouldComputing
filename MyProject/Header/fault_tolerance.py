
__author__ = 'yunlu'

import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
from Logger.custome_logger import get_logger
from SQS import handler as SQS_handler

import threading
import time



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
    to_check_list = static.get_busy()
    #for check_id in to_check_list:
        #instance_status_list = EC2_handler.get_instance_status(ec2,check_id)
        #instance_status = instance_status_list [0]['InstanceState']['Name']
    # get now working instance list
    compared_instance_list = EC2_handler.get_instance_running_worker(ec2)
    compared_instance_ID = EC2_handler.get_instanceId(compared_instance_list)
    # compare these lists, the result is the fault instances list
    not_match = [x for x in to_check_list if x not in compared_instance_ID]
    return not_match

def reboot_not_match(ec2,client,static,sqs):
    global valid
    while (valid):
        reboot_id_list = check_survive(ec2,static)
        #EC2_handler.start_instance(reboot_id_list)
        for instance_id in reboot_id_list:
            # get the job assigned to that id
            last_job = static.de_register_in_details(instance_id)
            header_IP = EC2_handler.get_local_ipv4()

            headloaction = header_IP +":9999"
            # bind the job with local ip
            msg= last_job +"#"+headloaction
            # put the job into the input queue again
            SQS_handler.create_msg(sqs, INPUT_QUEUE, msg)
        if len(reboot_id_list) >0:
            thread(EC2_handler.start_instance,client,reboot_id_list)
        time.sleep(5)
    #return response

            
def start_check_survive(ec2,client,static,sqs):
    #start the thread
    thread(reboot_not_match,ec2,client,static,sqs)

