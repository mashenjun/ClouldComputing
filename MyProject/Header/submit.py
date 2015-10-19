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
TIME_TO_CHECK=3
state_file=0
no_hit=0
logger = custome_logger.get_logger(__name__)
config = Config()

class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def update_changes_thread(ite_time):
    while(1):
        global state_file
        dir_state = DirState.from_json(state_file)
        dir_state2 = DirState(d)
        changes = dir_state2 - dir_state
        print changes
        #update the changes (no thread)
        new_files=changes["created"]
        print ("the new files are %s" % new_files)
        print (len(new_files))
        if (len(new_files)>0):
            S3_handler.send_files_head(new_files)
            print ("Have uploaded %i files" % len(new_files))
            #delete the files (no thread) (ignore at first)
            #change the json file
            global state_file
            state_file = dir_state2.to_json()
            time.sleep(ite_time) 
        else:
            time.sleep(2*ite_time)
            global no_hit
            no_hit+=1
            if (no_hit==5):
                break
        
        
#initial
d=S3_handler.set_dir_for_state()
dir_state = DirState(d)
state_file = dir_state.to_json()
#start the thread
submit_thread = thread(update_changes_thread, TIME_TO_CHECK)    