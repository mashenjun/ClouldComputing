__author__ = 'yunlu'

import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from os.path import join
from S3 import handler as S3_handler
from SQS import handler as SQS_handler
from Logger import custome_logger
from configFile.instanceConfig import Config
from EC2 import handler as EC2_handler
from dirtools import Dir, DirState
import threading
import time
import scheduler

no_hit = 0
logger = custome_logger.get_logger(__file__)
config = Config()


d = S3_handler.set_dir_for_state()
logger.debug(d)
dir_state = DirState(d)
state_file = dir_state.to_json()
old_state_file = state_file

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def update_changes_thread(ite_time,sqs):
    global LOCAL_QUEUE
    while(1):
        global state_file
        global old_state_file
        dir_state = DirState.from_json(state_file)
        dir_state2 = DirState(d)
        changes = dir_state2 - dir_state
        print changes
#        print(dir_state)
#        print(dir_state2)
        #update the changes (no thread)
        new_files=changes["created"]
        deleted_files = changes["deleted"]
        print ("the new files are %s" % new_files)
        print (len(new_files))
        if (len(new_files)>0):
            S3_handler.send_files_head(new_files)
            print ("Have uploaded %i files" % len(new_files))
            #change the json file
            old_state_file = state_file
            state_file = dir_state2.to_json()
            os.remove(old_state_file)
            #insert files into the scheduler
            scheduler.insert_new_job(new_files)
            logger.debug(scheduler.LOCAL_QUEUE)
            
            #invoke the scheduler and send the msg into sqs
            scheduler.send_message_to_sqs(sqs)
            time.sleep(ite_time)
        elif(len(deleted_files)>0):

            old_state_file = state_file
            state_file = dir_state2.to_json()
            os.remove(old_state_file)
        else:
            time.sleep(2*ite_time)
            #global no_hit
            #no_hit+=1
            #if (no_hit==10):
            #    break
        

def start_submit(time_to_check,sqs):
#initial
    #start the thread
    thread(update_changes_thread, time_to_check,sqs)
