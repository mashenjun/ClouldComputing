__author__ = 'mashenjun'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from SQS import handler as SQSHander

"""
Call
"""
sqs=SQSHander.connect_to_sqs()
#Create a msg in the TestSQS queue
#create_msg(sqs,'TestSQS','AHAHAH')

#receive the msg and print out the Body
client= SQSHander.get_client()
queue=SQSHander.get_queue(sqs,'Test')
msg=SQSHander.receive_msg(client,queue)
SQSHander.response(msg)

#delete the msg
#delete_msg(client,msg,queue)
