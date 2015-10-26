__author__ = 'mashenjun'

import Pyro4
import sys,os.path,time
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import EC2.cmdshell as ec2cmd
import EC2.handler as ec2h
import S3.handler as s3h
import SQS.handler as sqsh
from Logger.custome_logger import get_logger
from os import listdir
from os.path import isfile, join, dirname
from configFile.instanceConfig import Config

config = Config()
logger = get_logger(__file__)
IMAGE_FOLDER = "images"
IMAGE_RESULT_FOLDER = "imageResult"

MODULE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
ip = config.ConfigSectionMap()["head_ip"]
static = Pyro4.Proxy("PYRONAME:example.data_storage@"+ip+":9999")
s3 = s3h.connect_to_S3()

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def moniter_state(username):
    old = static.get_task_value(sys.argv[1])
    print "still "+str(old)+" tasks left"
    while (1):
        new = static.get_task_value(sys.argv[1])
        if new <= 0:
            static.del_task(username)
            break
        if old != new:
            print "still "+new+" tasks left"
            old = new
        time.sleep(1)
        print '\b.',
        sys.stdout.flush()

    print ("the task is finished ..... start fentch result")
    s3h.fentch_output(s3,username)
    s3h.delete_input(s3,username)
    s3h.delete_output(s3,username)
    print ("you can get the result under the imageresult file")

if __name__ == "__main__":
    thread(moniter_state,sys.argv[1])