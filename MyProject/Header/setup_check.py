__author__ = 'mashenjun'
import sys,os.path
import threading
import time
import static
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from SQS import handler as SQSHandler
from EC2 import handler as EC2Handler
from S3 import handler as S3Handler
from configFile.instanceConfig import Config
import Pyro4
from multiprocessing.pool import ThreadPool
import time

config = Config()
INPUT_QUEUE = config.ConfigSectionMap()["sqs_input_queue"]
OUTPUT_QUEUE = config.ConfigSectionMap()["sqs_output_queue"]
REMOTE_STORAGE_NAME = "PYRONAME"+config.ConfigSectionMap()["remote_storage_name"]

static = Pyro4.Proxy("PYRONAME:example.data_storage")
pool = ThreadPool(process=3)
finish = 0
# check the instance pool and setup system
# check instance number

def ec2_init():
    ec2, ec2_client = EC2Handler.connect_ec2()
    instance_num = EC2Handler.get_instance_num(ec2,False)
    workers = EC2Handler.get_instance_running_worker(ec2)
    static.add_to_idle.append(EC2Handler.get_instanceId(workers))
    if len(workers) < 2:
    # create instance from images
    # store the instance id
        instances = EC2Handler.create_instance_from_image(ec2,2-len(workers))
        for i in instances:
            counter = 0;
            EC2Handler.set_key_name(ec2,i._id,"Name","Worker"+str(counter+len(workers)))
            counter += counter
            static.add_to_idle.append(i._id)
    global finish
    finish +=1
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
    return (sqs, sqs_client)

def s3_init():
    s3 = S3Handler.connect_S3()
    S3Handler.create_bucket(s3)
    global finish
    finish +=1
    return(s3)

result1= pool.apply_async(ec2_init,())
result2= pool.apply_async(sqs_init,())
result3= pool.apply_async(s3_init,())

ec2,ec2_client = result1.get()
sqs, sqs_client = result2.get()
s3 = result3.get()

# check sqs

# check s3 check the bucket cloud-compute

# start the threads to listen the queue
while finish<3:
    time.sleep(1)










