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
from Static import static as static_handler
from EC2 import cmdshell as cmd_handler
import threading
import time

config = Config()
INPUT_QUEUE = config.ConfigSectionMap()["sqs_input_queue"]

state_file = 0
no_hit = 0
logger = custome_logger.get_logger(__name__)
config = Config()


d = S3_handler.set_dir_for_state()
dir_state = DirState(d)
state_file = dir_state.to_json()

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
        header_IP = EC2_handler.get_local_ipv4()
        if (len(new_files)>0):
            S3_handler.send_files_head(new_files)
            print ("Have uploaded %i files" % len(new_files))
            #assign the tasks to instance and update the static lists
            for single_file in new_files:
                #get a new idle instance ID
                selected_id=static_handler.get_idle()[0]
                #ssh to that id
                cmd_handler.get_instance(selected_id)
                #send msg in the queue
                sqs,client=SQS_handler.connect_sqs()
                #build the msg username/filename#header_IP
                msg = single_file.join("#",header_IP)
                #send msg to invoke the instance
                SQS_handler.create_msg(sqs,INPUT_QUEUE,msg)
                #move the instance to busy list
                static_handler.move_to_busy(selected_id)                              
            #delete the files (no thread),json (ignore at first)
            #change the json file
            global state_file
            state_file = dir_state2.to_json()
            time.sleep(ite_time) 
        else:
            time.sleep(2*ite_time)
            #global no_hit
            #no_hit+=1
            #if (no_hit==5):
            #    break
        

def start_submit(time_to_check):
#initial
    #start the thread
    submit_thread = thread(update_changes_thread, time_to_check)