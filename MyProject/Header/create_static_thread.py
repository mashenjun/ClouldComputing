__author__ = 'mashenjun'

import sys,os.path
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from SQS import handler as SQSHander
import Static.static_create as cs
from multiprocessing import Process, Value
import time

exitFlag = 0

def create():
    cs.create_static_data()


class create_static_Thread (threading.Thread):
    def __init__(self,):
        threading.Thread.__init__(self)

    def run(self):
        create()

def create_static():
    # Create new threads
    threading.Thread(target=create(), args=())
    #thread1 = create_static_Thread()
    # Start new Threads
    #thread1.start()
    #p = Process(target=create, args=())
    #p.start()
    print("rest codes running")

