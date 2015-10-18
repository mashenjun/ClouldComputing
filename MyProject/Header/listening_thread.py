__author__ = 'mashenjun'

import sys,os.path
import threading
import time

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from SQS import handler as SQSHander
import Static.static_create as create_static

create_static.create_static_data()

sqs,client = SQSHander.connect_sqs()
queue=SQSHander.get_queue(sqs,'TestSQS')

exitFlag = 0

def listening(threadName, delay, list_idle, list_busy):
    while True:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        msg_list =SQSHander.receive_multi_msg(client,queue,10)


class myThread (threading.Thread):
    def __init__(self, threadID, name,list_idle,list_busy):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.list_idle = list_idle
        self.list_busy = list_busy
    def run(self):
        listening(self.name, 1, self.list_idle,self.list_busy)

# Create new threads
thread1 = myThread(1, "Thread-1", 1)

# Start new Threads
thread1.start()


print "Exiting Main Thread"
