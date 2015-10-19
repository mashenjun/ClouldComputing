__author__ = 'mashenjun'

import Pyro4
import sys,os.path,time
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.cmdshell as ec2cmd
import S3.handler as s3h
import SQS.handler as sqsh
from os import listdir
from os.path import isfile, join, dirname
from configFile.instanceConfig import Config

config = Config()
IMAGE_FOLDER = "images"
IMAGE_RESULT_FOLDER = "imageResult"
MODULE_PATH = dirname(os.path.abspath(__file__))
mypath = join(MODULE_PATH,IMAGE_FOLDER)

static = Pyro4.Proxy("PYRONAME:example.data_storage")
sqs,sqs_client = sqsh.connect_sqs()
instanceid = static.get_idle[0]
ec2cmd.remove_from_idle(instanceid)
instance = ec2cmd.get_instance(instanceid)
ec2cmd.add_to_busy(instanceid)
ec2cmd.insert_new_task(sys.argv[1],sys.argv[2])
client = ec2cmd.ssh_to_instance(instance)
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for item in onlyfiles:
    sqsh.create_msg(sqs,"input",item)

status,stdout,stderr=ec2cmd.ssh_run_command(client,"python /home/ubuntu/MyProject/Worker/main.py")
print (stdout)

while static.get_task_value(sys.argv[1])!=0:
    time.sleep(1)
    print(".")

print("the task is finished .....")


