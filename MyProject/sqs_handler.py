"""
Created on Wed Oct  7 11:41:36 2015

@author: yun
"""

import boto3
import boto

"""
Definition
"""
from boto3.session import Session

session = Session(aws_access_key_id='AKIAJLKUUWG5UZCRNTCQ',
                  aws_secret_access_key='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',
                  region_name='eu-central-1')
                  
                  
def connect_to_s3():
	s3=session.resource('s3')
	return s3

def get_service_resource():
	sqs=session.resource('sqs')
	return sqs
 
def receive_msg(client,queue):
    msg=client.receive_message(QueueUrl=queue.url)
    return msg
    
def create_queue(sqs,queueName):
	taskq=sqs.create_queue(QueueName=queueName)
	return taskq

def get_queue(sqs,queueName):
	thisQueue=sqs.get_queue_by_name(QueueName=queueName)
	return thisQueue

def create_msg(sqs,queueName,msg):
	thisQueue=get_queue(sqs,queueName)
	thisQueue.send_message(MessageBody=msg)
 
def get_client():
	client=session.client('sqs')
	return client
    
def response(msg):
    msgBody=msg["Messages"][0]["Body"]   
    print msgBody
    
def delete_msg(client,msg,queue):
    msgHandle=msg["Messages"][0]["ReceiptHandle"] 
    response=client.delete_message(QueueUrl=queue.url,ReceiptHandle=msgHandle)
    return response
    
def delete_queue(client,queue):
    response=client.delete_queue(QueueUrl=queue.url)
    return response
    
def change_visibility(client,queue,msg,time):
    msgHandle=msg["Messages"][0]["ReceiptHandle"] 
    response=client.change_message_visibility(QueueUrl=queue.url,ReceiptHandle=msgHandle,VisibilityTimeout=time)
    return response

"""
Call
"""
s3=connect_to_s3()
sqs=get_service_resource()
#Create a msg in the TestSQS queue
#create_msg(sqs,'TestSQS','AHAHAH')

#receive the msg and print out the Body
client=get_client()
queue=get_queue(sqs,'TestSQS')
msg=receive_msg(client,queue)
response(msg)
change_visibility(client,queue,msg,120)

#delete the msg
#delete_msg(client,msg,queue)