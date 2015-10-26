__author__ = 'mashenjun'
import time,sys,os
import threading
import Pyro4
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.handler as ec2h
from Logger.custome_logger import get_logger
import Pyro4

logger = get_logger(__file__)

class deadline(object):
    num = 0
    valid = 1
    ec2,client = ec2h.connect_ec2()
    #static = Pyro4.Proxy("PYRONAME:example.data_storage@192.168.174.134:9999")

    def __init__(self, time,static):
        self.num = time
        self.static = static
        self.lock = threading.Lock()
        t=threading.Thread(target= self.countdown)
        t.start()


    def countdown(self):
        while ( self.num > 0):
            self.lock.acquire()
            try:
                self.num -= 1
                time.sleep(2)
            finally:
                self.lock.release()
            if self.valid == 0:
                logger.debug("I am Dead @ time :"+str(self.num))
                break
            if (self.num == 0):
                #launch a new instance
                instances = ec2h.create_instance_from_image(self.ec2,1,self.static)
                instanceid = ec2h.get_instanceId(instances)
                ec2h.set_key_name(self.ec2,instanceid[0],"Name","Worker"+str(self.static.get_sum()))
                logger.debug("create a new worker" + str(instances) + "deadline 0" )
                break

    def add_num(self, value):
        self.lock.acquire()
        try:
            self.num +=value
        finally:
            self.lock.release()

    def set_valid(self,num):
        self.valid = num

    def set_time(self,value):
        self.lock.acquire()
        try:
            self.num = value
        finally:
            self.lock.release()



