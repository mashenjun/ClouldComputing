__author__ = 'mashenjun'
import sys,os.path
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from SQS import handler as SQSHandler
from EC2 import handler as EC2Handler
from S3 import handler as S3Handler
from configFile.instanceConfig import Config
import Pyro4
from multiprocessing.pool import ThreadPool
import listening_thread
import time
import Auto_send_file
from Logger.custome_logger import get_logger,start_record_busy_workers
import backstage_scheduler
import fault_tolerance
import delete_worker

config = Config()
logger = get_logger(__file__)
INPUT_QUEUE = config.ConfigSectionMap()["sqs_input_queue"]
OUTPUT_QUEUE = config.ConfigSectionMap()["sqs_output_queue"]
REMOTE_STORAGE_NAME = "PYRONAME:"+config.ConfigSectionMap()["remote_storage_name"]
ip = config.ConfigSectionMap()["head_ip"]
LOCAL_QUEUE = {}
static = Pyro4.Proxy("PYRONAME:example.data_storage@"+ip+":9999")
pool = ThreadPool(processes=3)
finish = 0
start_time = time.clock()
# check the instance pool and setup system
# check instance number



def ec2_init():
    ec2, ec2_client = EC2Handler.connect_ec2()
    instance_num = EC2Handler.get_instance_num(ec2,True)
    stopped_workers = EC2Handler.get_stopped_worker(ec2)
    if (len(stopped_workers)>0 & len(instance_num)< 3):
        stopped_ID = EC2Handler.get_instanceId(stopped_workers)
        EC2Handler.start_instance(ec2_client,stopped_ID)

    workers = EC2Handler.get_instance_running_worker(ec2)
    logger.debug("the current workers is "+ str(workers))
    static.add_to_idle(EC2Handler.get_instanceId(workers))
    if len(workers) < 2:
    # create instance from images
    # store the instance id
        instances = EC2Handler.create_instance_from_image(ec2,2-len(workers),static)
        for i in instances:
            counter = len(workers)
            EC2Handler.set_key_name(ec2,i._id,"Name","Worker"+str(counter+len(workers)))
            counter += counter
            #static.add_to_idle(i._id)
    global finish
    finish +=1
    logger.debug("ec2_completet")
    return (ec2,ec2_client)

def sqs_init():
    sqs, sqs_client = SQSHandler.connect_sqs()
    queues_name = SQSHandler.get_all_queue_name(sqs)
    result = SQSHandler.check_queue_exist(queues_name)
    if result == 1:
        SQSHandler.create_queue(sqs,INPUT_QUEUE)
    elif result == 2:
        SQSHandler.create_queue(sqs,OUTPUT_QUEUE)
    global finish
    finish +=1
    logger.debug("sqs_completet")
    return (sqs, sqs_client)

def s3_init():
    s3 = S3Handler.connect_to_S3()
    S3Handler.create_bucket(s3)
    global finish
    finish +=1
    logger.debug("s3_completet")
    return(s3)

result1= pool.apply_async(ec2_init,())
result2= pool.apply_async(sqs_init,())
result3= pool.apply_async(s3_init,())

ec2,ec2_client = result1.get()
sqs, sqs_client = result2.get()
s3 = result3.get()

logger.debug("check complete")
# the above is ok

# check sqs

# check s3 check the bucket cloud-compute

# start the threads to listen the queue
while True:
    if finish>2:
        break



backstage_scheduler.start_backstage_scheduler(sqs,ec2,static)

listening_thread.create_run_listener(sqs,sqs_client,static)

Auto_send_file.start_submit(s3,1,static)

fault_tolerance.start_check_survive(ec2,ec2_client,static,sqs)

delete_worker.start_delete_worker(ec2,static)

start_record_busy_workers(static)










