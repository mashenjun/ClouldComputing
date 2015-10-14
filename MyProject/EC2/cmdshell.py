# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:16:20 2015

@author: yun
"""

import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance

#conn=boto.ec2.connect_to_region("eu-central-1")
#instance=conn.get_all_instances(instance_ids=['i-804dfb41'])[0].instances[0]
#ssh_client=sshclient_from_instance(instance,ssh_key_file='/home/yun/Documents/Cloudcomputing/mashenjun.pem',user_name='ubuntu')
#status,stdout,stderr=ssh_client.run('ls -al')
#ssh_client.put_file("/home/yun/Documents/Cloudcomputing/hello.py","/home/ubuntu/CloudComputing/hello.py")

def get_instance(conn,instance_id):
    instance=conn.get_all_instances(instance_ids=[instance_id])[0].instances[0]
    return instance
    
def ssh_to_instance(instance,key_path):
    ssh_client=sshclient_from_instance(instance,ssh_key_file=key_path,user_name='ubuntu')
    return ssh_client
    
def ssh_run_command(ssh_client,str_command):
    status,stdout,stderr=ssh_client.run(str_command)
    return (status, stdout, stderr)

def ssh_put_file(ssh_client,src_full,dst_full):
    ssh_client.put_file(src_full,dst_full)
    
    
"""
Application
"""
conn=boto.ec2.connect_to_region("eu-central-1")
instance=get_instance(conn,'i-804dfb41')
ssh_client=ssh_to_instance(instance,'/home/yun/Documents/Cloudcomputing/mashenjun.pem')
ssh_put_file(ssh_client,"/home/yun/Documents/Cloudcomputing/hello.py","/home/ubuntu/CloudComputing/hello.py")
status,stdout,stderr=ssh_run_command(ssh_client,"python /home/ubuntu/CloudComputing/hello.py")
print stdout