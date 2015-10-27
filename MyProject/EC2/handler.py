# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 06:11:53 2015

@author: yun
"""
import sys, os
import boto.utils
import threading
import time
from boto3.session import Session
from configFile.instanceConfig import Config
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger import custome_logger
from EC2 import cmdshell as ec2cmdshell

logger = custome_logger.get_logger("EC2.handler")
config = Config()
ACCESS_KEY_ID = config.ConfigSectionMap()["aws_access_key_id"]
SECRET_ACCESS_KEY = config.ConfigSectionMap()["aws_secret_access_key"]
VISIBILITY_TIME = config.ConfigSectionMap()["visibility_time"]
REGION_NAME = config.ConfigSectionMap()["region"]
AMI = config.ConfigSectionMap()["ami"]

session = Session(aws_access_key_id=ACCESS_KEY_ID,
                  aws_secret_access_key=SECRET_ACCESS_KEY,
                  region_name=REGION_NAME)

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def get_resource():
    ec2=session.resource('ec2')
    return ec2

def get_client():
    client=session.client('ec2')
    return client

def connect_ec2():
    ec2=get_resource()
    client=get_client()
    return (ec2,client)

def create_instance(ec2,numberofinstance):
    instances=ec2.create_instances(ImageId=AMI,MinCount=1,MaxCount=numberofinstance,
    KeyName='mashenjun',InstanceType='t2.micro',Monitoring={'Enabled':True},
    )
    return instances

def create_instance_from_image(ec2,numberofinstance,static):
    instances = ec2.create_instances(ImageId=AMI,MinCount=1,MaxCount=numberofinstance,
    KeyName='mashenjun',SecurityGroups=['launch-wizard-1'],InstanceType='t2.micro',Monitoring={'Enabled':True},
    )
    #get instanceIds list 
    instanceIds = get_instanceId(instances)
    #add the Ids list to the idle list
    #static.add_to_idle(instanceIds)
    #create a thread for each instance to wait until they finish initializing
    for instanceId in instanceIds:
        thread(wait_worker_init,ec2,static,instanceId)
    return instances

def terminate_instance(ec2,instanceid):
    instance=ec2.get_all_instances(instance_ids=[instanceid])[0].instances[0]
    instance.terminate()

def get_instanceId(instances):
    instanceIds = [r._id for r in instances]
    return instanceIds


def set_key_name(ec2,instanceId,key,value):
    response=ec2.create_tags(Resources=[instanceId,],Tags=[{'Key':key,'Value':value},])
    return response


def start_instance(client,instanceId):
    response=client.start_instances(InstanceIds=instanceId)
    return response

def stop_instance(client,instanceId):
    response=client.stop_instances(InstanceIds=instanceId)
    return response

def get_instance_num(ec2, running):
    if running == False:
        instances = ec2.instances.filter()
    else :
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    return list(instances)

# instanceid is list
def get_instance_status(ec2,instanceid):
    return ec2.meta.client.describe_instance_status(InstanceIds =[instanceid])['InstanceStatuses']

def get_instance_worker(ec2):
    instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:Name', 'Values': ["Worker*"]}])
    return list(instances)

def get_instance_running_worker(ec2):
    instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:Name', 'Values': ["Worker*"]},{'Name': 'instance-state-name', 'Values': ['running','pending']}])
    return list(instances)

def get_instance_stopped_worker(ec2):
    instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:Name', 'Values': ["Worker*"]},{'Name': 'instance-state-name', 'Values': ['stopped','stopping']}])
    return list(instances)

def get_local_instanceId():
    region = boto.utils.get_instance_metadata()
    return region["instance-id"]

def get_local_ipv4():
    region = boto.utils.get_instance_metadata()
    return region["local-ipv4"]

def wait_worker_init(ec2,static,instanceId):
    # check the state of instance
    # wait until it is running
    static.add_pending(instanceId)
    while(not get_instance_status(ec2,instanceId)):
        time.sleep(2)
    instance = ec2cmdshell.get_instance(instanceId)
    ec2cmdshell.ssh_to_instance(instance)
    static.move_from_pending_to_idle(instanceId)
"""
Application
"""
def main():
    ec2=get_resource()
    instance=create_instance(ec2,1)
    instanceId=get_instanceId(instance)
    set_key_name(ec2,instanceId,'Name','Worker4')
    client=get_client()

    stop_instance(client,instanceId)

    start_instance(client,instanceId)

if __name__ == "__main__":
    main()
