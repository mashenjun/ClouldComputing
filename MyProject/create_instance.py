# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 06:11:53 2015

@author: yun
"""

import boto3
import boto

def get_resource():
    ec2=boto3.resource('ec2')
    return ec2    

def create_instance(ec2,numberofinstance):
    instance=ec2.create_instances(ImageId='ami-accff2b1',MinCount=1,MaxCount=numberofinstance,
    KeyName='mashenjun',InstanceType='t2.micro',Monitoring={'Enabled':True},
    NetworkInterfaces=[{'DeviceIndex':0,'AssociatePublicIpAddress':True},])
    return instance
    
def get_InstanceId(instance):
    instanceId=instance[0]._id
    return instanceId
        
    
def set_key_name(ec2,instanceId,key,value):
    response=ec2.create_tags(Resources=[instanceId,],Tags=[{'Key':key,'Value':value},])
    return response

def get_client():
    client=boto3.client('ec2')
    return client    
        
def start_instance(client,instanceId):
    response=client.start_instances(InstanceIds=[instanceId])
    return response
    
def stop_instance(client,instanceId):
    response=client.stop_instances(InstanceIds=[instanceId])
    return response
    
"""
Application
"""
ec2=get_resource()
instance=create_instance(ec2,1)
instanceId=get_InstanceId(instance)
set_key_name(ec2,instanceId,'Name','Worker4')
client=get_client()

stop_instance(client,instanceId)

start_instance(client,instanceId)