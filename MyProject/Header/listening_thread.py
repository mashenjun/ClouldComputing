__author__ = 'yunlu'

import sys,os.path
import threading
import time

#import static
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from configFile.instanceConfig import Config
from SQS import handler as SQSHandler
from SQS import message_process
from Logger.custome_logger import get_logger
import scheduler
import Pyro4
#import Static.static_create as create_static
#import Static.static_handler as Shandler

#create_static()
config = Config()
logger = get_logger(__file__)
OUTPUT_QUEUE = config.ConfigSectionMap()["sqs_output_queue"]
REMOTE_STORAGE_NAME = "PYRONAME"+config.ConfigSectionMap()["remote_storage_name"]


exitFlag = 0


def listening(threadName, sqs,client, delay, static ):

    queue = SQSHandler.get_queue(sqs, OUTPUT_QUEUE)
    while True:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        msg=SQSHandler.receive_multi_msg(client, queue, 1)

        if (len(msg)>1):
            msg_content=SQSHandler.response(msg)
            user = message_process.message_getusername(msg_content)
            instanceID = message_process.message_gerid(msg_content)
            logger.debug("reveive a message in output queue with "+user)
            static.minus_task(user)
            static.move_to_idle(instanceID)
            scheduler.send_message_to_sqs(sqs)
            SQSHandler.delete_msg(client,msg,queue)
            if (static.get_task_value(user)==0):
                print "user %s could fetch now " % user
                #user_t = fetch_data(wait_finish,user) #url
        else:
            print "No msg now"
            time.sleep(3*delay)
#        SQSHandler.delete_msg(client, msg, queue)
        

class listen_thread(threading.Thread):
    def __init__(self, threadID, name, sqs, client, static):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.sqs = sqs
        self.client = client
        self.static = static
    def run(self):
        listening(self.name,self.sqs, self.client,1,self.static)
          
class fetch_data(threading.Thread):
    #url
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def wait_finish(user):
    time.sleep(5) 
    print "user %s is finished now " % user         

def create_run_listener(sqs,client,static):
    thread1 = listen_thread(1, "listener",sqs,client,static)
    # Start new Threads
    thread1.start()







