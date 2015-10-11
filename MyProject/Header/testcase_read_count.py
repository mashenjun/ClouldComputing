__author__ = 'mashenjun'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
from SQS import handler as SQS_handler



logger = custome_logger.get_logger(__name__)
config = Config()
BUCKET_NAME = config.ConfigSectionMap()["bucket_name"]
conn_SQS = SQS_handler.connect_to_sqs()
queue = SQS_handler.get_queue(conn_SQS,BUCKET_NAME)
count = SQS_handler.get_queue_count(queue)
logger.info(count)