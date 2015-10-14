

import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.handler as EC2handler
import EC2.cmdshell as EC2cmd
from Logger import custome_logger
from configFile.instanceConfig import Config


config = Config()
logger = custome_logger.get_logger(__name__)

ec2 = EC2handler.connect_ec2()
