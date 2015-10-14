__author__ = 'mashenjun'
import sys,os.path
import threading
import time
import static
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from SQS import handler as SQSHandler
from EC2 import handler as EC2Handler

import Static.static_create as create_static
# check the instance pool and setup system
# check instance number
ec2, ec2_client = EC2Handler.connect_ec2()
instance_num = EC2Handler.get_instance_num(ec2)
if instance_num < 0:
    print()

# check sqs
# check s3

