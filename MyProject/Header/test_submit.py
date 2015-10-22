__author__ = 'mashenjun'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.cmdshell as ec2cmd

instanceid = "i-019846bd"
instance = ec2cmd.get_instance(instanceid)
ssh_client = ec2cmd.ssh_to_instance(instance)
status,stdout,stderr=ec2cmd.ssh_run_command(ssh_client,"python /home/ubuntu/MyProject/Worker/main.py")
