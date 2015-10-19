

import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.handler as EC2handler
import EC2.cmdshell as EC2cmd
from Logger import custome_logger
from configFile.instanceConfig import Config


config = Config()
logger = custome_logger.get_logger(__name__)
KEY_PATH = config.ConfigSectionMap()["path_to_key"]

instance = EC2cmd.get_instance("i-6c77a1d0")
ssh_client = EC2cmd.ssh_to_instance(instance)
status,stdout,stderr=EC2cmd.ssh_run_command(ssh_client,"python /home/ubuntu/MyProject/Worker/main.py")
print (stderr)