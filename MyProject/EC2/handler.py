# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 06:11:53 2015

@author: yun
"""
import sys, os
import boto.utils
import threading
import time
import socket
from boto3.session import Session
from configFile.instanceConfig import Config
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger import custome_logger
from EC2 import cmdshell as ec2cmdshell
import Metrix.timemetrix as mt

logger = custome_logger.get_logger("EC2.handler")
instancelogger = custome_logger.get_launch_new_instance_time_logger("launch_instance")
elasticlogger = custome_logger.get_elastic_logger("elastic_scalling")
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
        elasticlogger.debug(str(time.time() - mt.setup_start_wall_time) + " : launch a new instance to " + str(static.get_all_workers_num()))
        thread(wait_worker_init,ec2,static,instanceId)
    return instances

def terminate_instance(ec2,instanceid,static):
    static.remove_from_idle(instanceid)
    ec2.instances.filter(InstanceIds=[instanceid]).stop()
    elasticlogger.debug(str(time.time() - mt.setup_start_wall_time) + " : terminate an instance to " + str(static.get_all_workers_num))

def get_instanceId(instances):
    instanceIds = [r._id for r in instances]
    return instanceIds


def set_key_name(ec2,instanceId,key,value):
    response=ec2.create_tags(Resources=[instanceId,],Tags=[{'Key':key,'Value':value},])
    return response


def start_instance(client, instanceId):
    if isinstance(instanceId, list):
        response=client.start_instances(InstanceIds=instanceId)
    else :
        response=client.start_instances(InstanceIds=[instanceId])
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

def get_stopped_worker(ec2):
    instances = ec2.instances.filter(
            Filters=[{'Name': 'tag:Name', 'Values': ["Worker*"]},{'Name': 'instance-state-name', 'Values': ['stopped']}])
    return list(instances)


def get_local_instanceId():
    region = boto.utils.get_instance_metadata()
    return region["instance-id"]

def get_local_ipv4():
    region = boto.utils.get_instance_metadata()
    return region["local-ipv4"]

def socket_check(instanceId):
    ec2client = get_client()
    response = ec2client.describe_instances(InstanceIds =[instanceId])
    clientip= response ['Reservations'][0]['Instances'][0]['PrivateDnsName'].split('.')[0]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((clientip, 22))
        print "Port 22 reachable"
        result = True
    except socket.error as e:
        print "Error on connect: %s" % e
        result = False
    s.close()
    return result


def wait_worker_init(ec2,static,instanceId):
    # check the state of instance
    # wait until it is running
    static.add_pending(instanceId)
    mt.launch_new_instance_process_time[instanceId] = time.clock()
    mt.launch_new_instance_wall_time[instanceId] = time.time()
    while(not get_instance_status(ec2,instanceId)):
        time.sleep(2)
    while (not socket_check(instanceId)):
        time.sleep(3)
    #instance = ec2cmdshell.get_instance(instanceId)
    #ec2cmdshell.ssh_to_instance(instance)
    instancelogger.debug(str(instanceId) + " process time : " + str(time.clock() - mt.launch_new_instance_process_time[instanceId]))
    instancelogger.debug(str(instanceId) + " wall time : " + str(time.time() - mt.launch_new_instance_wall_time[instanceId]))
    static.move_from_pending_to_idle(instanceId)
    static.decrease_pending_compensate()
    if (static.get_pending_num() == 0):
        static.reset_pending_compensate()

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
