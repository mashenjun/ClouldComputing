__author__ = 'mashenjun'

from SQS import handler as SQSHander

"""
Call
"""
sqs=SQSHander.get_service_resource()
#Create a msg in the TestSQS queue
#create_msg(sqs,'TestSQS','AHAHAH')

#receive the msg and print out the Body
client= SQSHander.get_client()
queue=SQSHander.get_queue(sqs,'TestSQS')
msg=SQSHander.receive_msg(client,queue)
SQSHander.response(msg)

#delete the msg
#delete_msg(client,msg,queue)
