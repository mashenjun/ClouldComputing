__author__ = 'yunlu'

import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
from Logger.custome_logger import get_logger

import threading
import time


logger = get_logger(__file__)
config = Config()
valid = 1

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def check_survive(ec2,static):
    # get both the idle instances number and the waiting tasks
    to_check_list = static.get_busy()
    #for check_id in to_check_list:
        #instance_status_list = EC2_handler.get_instance_status(ec2,check_id)
        #instance_status = instance_status_list [0]['InstanceState']['Name']
    compared_instance_list = EC2_handler.get_instance_running_worker(ec2)
    compared_instance_ID = EC2_handler.get_instanceId(compared_instance_list)
    not_match = [x for x in to_check_list if x not in compared_instance_ID]
    return not_match

def reboot_not_match(ec2,static):
    global valid
    while (valid):
        reboot_id_list = check_survive(ec2,static)
        #EC2_handler.start_instance(reboot_id_list)
        thread(EC2_handler.start_instance,reboot_id_list)
        time.sleep(5)
    #return response

            
def start_check_survive(ec2,static):
    #start the thread
    thread(reboot_not_match,ec2,static)