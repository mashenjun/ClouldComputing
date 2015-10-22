__author__ = 'mashenjun'
import time,sys,os
import threading
import Pyro4
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.handler as ec2h


class deadline(object):
    num = 0
    valid = 1
    ec2,client = ec2h.connect_ec2()
    def __init__(self, time, static):
        self.num = time
        self.static = static
        t=threading.Thread(target= self.countdown)
        t.start()

    def countdown(self):
        while ( self.num > 0):
            self.num -= 1
            time.sleep(1)
            if self.valid == 0:
                break
        if (self.num == 0) :
            #launch a new instance
            instances = ec2h.create_instance_from_image(self.ec2,1)
            self.static.add_to_idle(ec2h.get_instanceId(instances))


    def add_num(self, value):
        self.num +=value


