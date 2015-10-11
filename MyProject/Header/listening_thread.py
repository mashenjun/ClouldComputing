__author__ = 'mashenjun'

import sys,os.path
import threading
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from SQS import handler as SQSHander

sqs=SQSHander.get_service_resource()
client= SQSHander.get_client()
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
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

print "Exiting Main Thread"
