__author__ = 'yunlu'

import sys,os.path
import threading
import time

#import static
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from configFile.instanceConfig import Config
from SQS import handler as SQSHandler
import Pyro4
#import Static.static_create as create_static
#import Static.static_handler as Shandler

#create_static()
config = Config()
OUTPUT_QUEUE = config.ConfigSectionMap()["sqs_output_queue"]
REMOTE_STORAGE_NAME = "PYRONAME"+config.ConfigSectionMap()["remote_storage_name"]


exitFlag = 0


def listening(threadName, sqs,client, delay,static ):

    queue = SQSHandler.get_queue(sqs, OUTPUT_QUEUE)
    while True:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        msg=SQSHandler.receive_multi_msg(client, queue, 1) 
        if (len(msg)>1):
            user=SQSHandler.response(msg)
            print user
            static.minus_task(user)
            print dict
            if (static.get_task_value[user]==0):
                print "user %s could fetch now " % user
                user_t = fetch_data(wait_finish,user) #url
        else:
            print "No msg now"
            time.sleep(3*delay)
#        SQSHandler.delete_msg(client, msg, queue)
        

class listen_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        listening(self.name, 1)
          
class fetch_data(threading.Thread):
    #url
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def wait_finish(user):
    time.sleep(5) 
    print "user %s is finished now " % user         
# Create new threads
thread1 = listen_thread(1, "Thread-1")

# Start new Threads
thread1.start()







