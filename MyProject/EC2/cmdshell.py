# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:16:20 2015

@author: yun
"""

import boto.ec2
import socket
from boto.manage.cmdshell import sshclient_from_instance
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from configFile.instanceConfig import Config
from Logger import custome_logger
from boto.ec2.connection import EC2Connection
config = Config()
logger = custome_logger.get_logger("cmdshell")
KEY_PATH = config.ConfigSectionMap()["path_to_key"]
EC2_ACCESS_KEY = config.ConfigSectionMap()["aws_access_key_id"]
EC2_SECRET_KEY = config.ConfigSectionMap()["aws_secret_access_key"]
REGION = "eu-central-1"

path = os.path.join(os.path.dirname(__file__), os.path.pardir)
KEY_PATH = os.path.join(path, "mashenjun.pem")

#conn=boto.ec2.connect_to_region("eu-central-1")
#instance=conn.get_all_instances(instance_ids=['i-804dfb41'])[0].instances[0]
#ssh_client=sshclient_from_instance(instance,ssh_key_file='/home/yun/Documents/Cloudcomputing/mashenjun.pem',user_name='ubuntu')
#status,stdout,stderr=ssh_client.run('ls -al')
#ssh_client.put_file("/home/yun/Documents/Cloudcomputing/hello.py","/home/ubuntu/CloudComputing/hello.py")

CONN_EC2 = boto.ec2.connect_to_region(REGION,
    aws_access_key_id=EC2_ACCESS_KEY,
    aws_secret_access_key=EC2_SECRET_KEY)


def get_instance(instance_id):
    instance = CONN_EC2.get_all_instances(instance_ids=[instance_id])[0].instances[0]
    return instance


def ssh_to_instance(instance):
    ssh_client = sshclient_from_instance(instance,ssh_key_file=KEY_PATH,user_name='ubuntu')
    return ssh_client
    
def ssh_run_command(ssh_client,str_command):
    status,stdout,stderr=ssh_client.run(str_command)
    return (status, stdout, stderr)

def ssh_put_file(ssh_client,src_full,dst_full):
    ssh_client.put_file(src_full,dst_full)



"""
Application
"""

def main():
    conn=boto.ec2.connect_to_region("eu-central-1")
    #instance=get_instance(conn,'i-804dfb41')
    #ssh_client=ssh_to_instance(instance,'/home/yun/Documents/Cloudcomputing/mashenjun.pem')
    #ssh_put_file(ssh_client,"/home/yun/Documents/Cloudcomputing/hello.py","/home/ubuntu/CloudComputing/hello.py")
    #status,stdout,stderr=ssh_run_command(ssh_client,"python /home/ubuntu/CloudComputing/hello.py")
    #print stdout

if __name__ == "__main__":
    main()