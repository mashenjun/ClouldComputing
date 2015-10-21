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

mypath = join(MODULE_PATH,IMAGE_FOLDER,sys.argv[1])
logger.debug("mypath is "+ mypath)
#LOCALIP = ec2h.get_local_ipv4()

static = Pyro4.Proxy("PYRONAME:example.data_storage@192.168.174.134:9999")
sqs,sqs_client = sqsh.connect_sqs()
static.insert_new_task(sys.argv[1],int(sys.argv[2]))
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]
logger.debug(mypath)
logger.debug("onlyfiles"+str(len(onlyfiles)))
for item in onlyfiles:
    instanceid = static.get_idle()[0]
    static.remove_from_idle(instanceid)
    static.add_to_busy(instanceid)
    #sqsh.create_msg(sqs,"input",item+"#"+str(LOCALIP))
    sqsh.create_msg(sqs,"input",join(sys.argv[1],item))
    logger.debug("successfully send a message")
    thread(tell_worker_to_run, instanceid)


while static.get_task_value(sys.argv[1])!=0:
    time.sleep(1)
    print '\b.',
    sys.stdout.flush()


print("the task is finished .....")




