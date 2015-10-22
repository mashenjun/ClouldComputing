__author__ = 'mashenjun'

import Pyro4
import sys,os.path,time
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.cmdshell as ec2cmd
import EC2.handler as ec2h
import S3.handler as s3h
import SQS.handler as sqsh
from Logger.custome_logger import get_logger
from os import listdir
from os.path import isfile, join, dirname
from configFile.instanceConfig import Config

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def tell_worker_to_run(instanceid):
    instance = ec2cmd.get_instance(instanceid)
    ssh_client = ec2cmd.ssh_to_instance(instance)
    status,stdout,stderr=ec2cmd.ssh_run_command(ssh_client,"python /home/ubuntu/MyProject/Worker/main.py")
    print (stdout)
    print (stderr)

config = Config()
logger = get_logger(__file__)
IMAGE_FOLDER = "images"
IMAGE_RESULT_FOLDER = "imageResult"


MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))


static = Pyro4.Proxy("PYRONAME:example.data_storage@192.168.174.134:9999")



while static.get_task_value(sys.argv[1])!=0:
    time.sleep(1)
    print '\b.',
    sys.stdout.flush()


print("the task is finished .....")