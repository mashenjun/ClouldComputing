__author__ = 'mashenjun'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import imageProcess, imageHandler
from os.path import join
from S3 import handler as S3_handler
from SQS import handler as SQS_handler
from SQS import message_process as SQS_mp
from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
import update_static as us
config = Config()
logger = custome_logger.get_logger(__name__)

conn_s3 = S3_handler.connect_to_S3()
conn_sqs,client = SQS_handler.connect_sqs()

INPUT_QUEUE_NAME = config.ConfigSectionMap()["sqs_input_queue"]
OUTPUT_QUEUE_NAME = config.ConfigSectionMap()["sqs_output_queue"]

#Create a msg in the TestSQS queue
#create_msg(sqs,'TestSQS','AHAHAH')
#receive the msg and print out the Body
input_queue=SQS_handler.get_queue(conn_sqs,INPUT_QUEUE_NAME)
msg=SQS_handler.receive_msg(client,input_queue)
msg_content = SQS_handler.response(msg)

#may change later
# header_Ip = SQS_mp.message_getip(msg_content)
message_list,HeaderIP = SQS_mp.message_getip(msg_content)
us.update_static(message_list,HeaderIP)
response = SQS_handler.delete_msg(client,msg,input_queue)
logger.debug("worker delete msg  state: " + str(response))

name = message_list.split("/")[0]
filename = message_list.split("/")[1]
#msg_list = message_process.message_process(msg)
S3_handler.get_file(conn_s3,name,filename)
imageProcess.process_image(filename)
S3_handler.send_file(conn_s3,name)
S3_handler.clear_local_folder()
my_instanceId=EC2_handler.get_local_instanceId()
SQS_handler.create_msg(conn_sqs, OUTPUT_QUEUE_NAME,join(name,filename)+"@"+my_instanceId)
us.del_static(HeaderIP)


