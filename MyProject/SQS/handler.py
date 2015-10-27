import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from boto3.session import Session
from configFile.instanceConfig import Config

from Logger.custome_logger import get_logger
config = Config()
logger = get_logger("SQS.handler")
ACCESS_KEY_ID = config.ConfigSectionMap()["aws_access_key_id"]
SECRET_ACCESS_KEY = config.ConfigSectionMap()["aws_secret_access_key"]
VISIBILITY_TIME = config.ConfigSectionMap()["visibility_time"]
REGION_NAME = 'eu-central-1'
INPUT_QUEUE = config.ConfigSectionMap()["sqs_input_queue"]
OUTPUT_QUEUE = config.ConfigSectionMap()["sqs_output_queue"]

session = Session(aws_access_key_id=ACCESS_KEY_ID,
                  aws_secret_access_key=SECRET_ACCESS_KEY,
                  region_name=REGION_NAME)


def connect_sqs():
    sqs = get_resource()
    client = get_client()
    return sqs,client

def get_resource():
    sqs = session.resource('sqs')
    return sqs

def get_client():
    client = session.client('sqs')
    return client

def create_queue(sqs, queueName):
    taskq = sqs.create_queue(QueueName=queueName, Attributes={'VisibilityTimeout': '0'})
    return taskq

def get_queue(sqs, queueName):
    thisQueue = sqs.get_queue_by_name(QueueName=queueName)
    return thisQueue

def get_all_queue_name(sqs):
    return [queue.attributes['QueueArn'].split(':')[-1] for queue in get_all_queue(sqs)]

def get_all_queue(sqs):
    return sqs.queues.all()

def check_queue_exist(list):
    if INPUT_QUEUE and OUTPUT_QUEUE in list:
        return 0
    elif OUTPUT_QUEUE in list:
        return 1
    elif INPUT_QUEUE in list:
        return 2

def receive_msg(client, queue):
    msg = client.receive_message(QueueUrl=queue.url)
    if len(msg)>1:
        change_visibility(client,queue,msg,60)
    return msg

def receive_multi_msg(client, queue, num):
    msg = client.receive_message(QueueUrl=queue.url, MaxNumberOfMessages=num)
    if len(msg)>1:
        change_visibility(client,queue,msg,60)
    return msg

def create_msg(sqs, queueName, msg):
    thisQueue = get_queue(sqs, queueName)
    thisQueue.send_message(MessageBody=msg)


def response(msg):
    msgBody = msg["Messages"][0]["Body"]
    return msgBody


def delete_msg(client, msg, queue):
    msgHandle = msg["Messages"][0]["ReceiptHandle"]
    response = client.delete_message(QueueUrl=queue.url, ReceiptHandle=msgHandle)
    return response


def delete_queue(client, queue):
    response = client.delete_queue(QueueUrl=queue.url)
    return response


def change_visibility(client, queue, msg, time):
    msgHandle = msg["Messages"][0]["ReceiptHandle"]
    response = client.change_message_visibility(QueueUrl=queue.url, ReceiptHandle=msgHandle, VisibilityTimeout=time)
    return response

def get_queue_count(queue):
    return queue.attributes.get("ApproximateNumberOfMessages")

