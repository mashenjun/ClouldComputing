__author__ = 'mashenjun'
import sys,os.path

sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.cmdshell as ecmd
import EC2.handler as EC2Handler

ec2 = EC2Handler.connect_ec2()
