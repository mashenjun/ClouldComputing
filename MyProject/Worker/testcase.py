__author__ = 'mashenjun'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import imageProcess
from S3 import handler as S3_handler
from SQS import handler as SQS_handler
from Logger import custome_logger
from configFile.instanceConfig import Config


config = Config()
logger = custome_logger.get_logger(__name__)

conn_s3 = S3_handler.connect_to_S3()
conn_sqs = SQS_handler.connect_to_sqs()

BUCKET_NAME = config.ConfigSectionMap()["bucket_name"]
#Create a msg in the TestSQS queue
#create_msg(sqs,'TestSQS','AHAHAH')

#receive the msg and print out the Body
client= SQS_handler.get_client()
queue=SQS_handler.get_queue(conn_sqs,BUCKET_NAME)
msg=SQS_handler.receive_msg(client,queue)
msg = SQS_handler.response(msg)
logger.info(msg)
message_list = msg.split("/")
name = message_list[1]
filename = message_list[2]
#msg_list = message_process.message_process(msg)
logger.info(len(message_list))
S3_handler.get_file(conn_s3,name,filename)
imageProcess.process_image(filename)
S3_handler.send_file(conn_s3,name)
S3_handler.clear_local_folder()
SQS_handler.delete_msg(msg)
