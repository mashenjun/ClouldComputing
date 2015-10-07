from boto3.session import Session
from configFile.instanceConfig import Config

config = Config()
ACCESS_KEY_ID = config.ConfigSectionMap()["aws_access_key_id"]
SECRET_ACCESS_KEY = config.ConfigSectionMap()["aws_secret_access_key"]
REGION_NAME = 'eu-central-1'

session = Session(aws_access_key_id=ACCESS_KEY_ID,
                  aws_secret_access_key=SECRET_ACCESS_KEY,
                  region_name=REGION_NAME)


def get_service_resource():
    sqs = session.resource('sqs')
    return sqs


def receive_msg(client, queue):
    msg = client.receive_message(QueueUrl=queue.url)
    return msg


def create_queue(sqs, queueName):
    taskq = sqs.create_queue(QueueName=queueName)
    return taskq


def get_queue(sqs, queueName):
    thisQueue = sqs.get_queue_by_name(QueueName=queueName)
    return thisQueue


def create_msg(sqs, queueName, msg):
    thisQueue = get_queue(sqs, queueName)
    thisQueue.send_message(MessageBody=msg)


def get_client():
    client = session.client('sqs')
    return client


def response(msg):
    msgBody = msg["Messages"][0]["Body"]
    print msgBody


def delete_msg(client, msg, queue):
    msgHandle = msg["Messages"][0]["ReceiptHandle"]
    response = client.delete_message(QueueUrl=queue.url, ReceiptHandle=msgHandle)
    return response


def delete_queue(client, queue):
    response = client.delete_queue(QueueUrl=queue.url)
    return response