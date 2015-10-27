__author__ = 'mashenjun'
import Pyro4
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger.custome_logger import get_logger
from configFile.instanceConfig import Config
from SQS import handler as SQS_handler
from EC2 import cmdshell as cmd_handler
from EC2 import handler as EC2_handler
import deadline
import Pyro4


config = Config()
logger = get_logger(__file__)
INPUT_QUEUE = config.ConfigSectionMap()["sqs_input_queue"]

LOCAL_QUEUE = {}
KEY_PATH = config.ConfigSectionMap()["path_to_key"]
ip = config.ConfigSectionMap()["head_ip"]
add_static = Pyro4.Proxy("PYRONAME:example.data_storage@"+ip+":9999")
LOCAL_NEW_FILES = {}



def insert_new_job(new_files,static):
    global LOCAL_NEW_FILES
    LOCAL_NEW_FILES = {}
    map(insert_single_job,new_files)
    logger.debug("-----------------------------the LOCAL_NEW_FILES is: " + str(LOCAL_NEW_FILES))
    #refresh the task queue
    for user in LOCAL_NEW_FILES.keys():
        #static.insert_new_task(user,return_users_tasks(user,static))
        #LOCAL_QUEUE[user]['Deadline'].set_time(LOCAL_QUEUE[user]['Counter'])
        #LOCAL_QUEUE[user]['Deadline']=deadline.deadline(LOCAL_QUEUE[user]['Counter'],static)
        static.insert_new_task(user,LOCAL_NEW_FILES[user])
        logger.debug("-----------------------------insert_new_task: " +str(LOCAL_NEW_FILES[user]))
        if (not LOCAL_QUEUE[user].has_key('Deadline')):
            LOCAL_QUEUE[user]['Deadline'] = deadline.deadline(LOCAL_NEW_FILES[user]*3,static)
        else:
            LOCAL_QUEUE[user]['Deadline'].add_num(LOCAL_NEW_FILES[user]*3)
    logger.debug("------------------------------LOCAL_QUEUE is" + str(LOCAL_QUEUE))
    logger.debug("-----------------------------the task dict is: " +str(static.get_task()))
    #result = [insert_new_job(p, p) for p in new_files]

def insert_single_job(file):
    global LOCAL_QUEUE
    global LOCAL_NEW_FILES
    user_name = file.split('/')[0]
    if (not LOCAL_QUEUE.has_key(user_name)):
        #LOCAL_QUEUE[user_name]={'Tasks':[],'Counter':0,'Deadline':deadline.deadline(99999)}
        LOCAL_QUEUE[user_name]={'Tasks':[],'Counter':0}
    if (not LOCAL_NEW_FILES.has_key(user_name)):
        LOCAL_NEW_FILES[user_name] = 0
    user_dic = LOCAL_QUEUE[user_name]
    user_dic['Tasks'].append(file)
    user_dic['Counter'] += 1
    LOCAL_NEW_FILES[user_name] += 1

def return_task():
    global LOCAL_QUEUE

    #logger.debug(user_list)
    if len(LOCAL_QUEUE.keys()) == 0:
        return None
    else:
        logger.debug(str(LOCAL_QUEUE))
        user_old = {k:v for k,v in LOCAL_QUEUE.items() if v.has_key('Deadline')}
        print ("user_old is: " + str(user_old))
        user_list = sorted(user_old.keys(),key = lambda e:user_old[e]['Deadline'].num)
        print ("user_list is: " + str(user_list))
        #user_list = sorted(LOCAL_QUEUE.keys(),key = lambda e:LOCAL_QUEUE[e]['Deadline'].num)
        #user_tasks = LOCAL_QUEUE[user_list[0]]['Tasks']
        if len(user_list) == 0:
            return None
        else:
            user_tasks = user_old[user_list[0]]['Tasks']
            user_name = user_list[0]
            if len(user_tasks) >1:
                return user_tasks.pop(0)
            elif len(user_tasks) == 1:
                #LOCAL_QUEUE[user_name]['Deadline'].set_valid(0)
                LOCAL_QUEUE[user_name]['Deadline'].set_valid(0)
                #logger.debug("*********************the valid num is: " + str(LOCAL_QUEUE[user_name]['Deadline'].valid))
                #user_dict = LOCAL_QUEUE.pop(user_name,None)
                user_dict = LOCAL_QUEUE.pop(user_name,None)
                #user_deadline = user_dict['Deadline']
                #user_deadline.set_valid(0)
                user_tasks = user_dict['Tasks']

                return user_tasks.pop(0)
            else:
                return None

def send_message_to_sqs(sqs,static):
    # get the length of idle list
    num_idle = len(static.get_idle())
    #logger.debug(num_idle)
    header_IP = EC2_handler.get_local_ipv4()
    #header_IP ="192.168.174.134"
    header_Port = "9999"
    header_location = header_IP+":"+header_Port
    # iterate the idle and assign the jobs to the idle worker until there are no tasks in local queue or no workers
    for i in range(0,num_idle):
        selected_job = return_task()
        #logger.debug(selected_job)
        if selected_job is None:
            break
        else:
            logger.debug("send message to worker ")
            selected_id=static.get_idle()[0]
            #move the instance to busy list
            static.move_to_busy(selected_id)
            #ssh to that id
            cmd_handler.get_instance(selected_id)
            #build the msg username/filename#header_IP
            msg = selected_job +"#"+header_location
            #send msg to invoke the instance
            SQS_handler.create_msg(sqs,INPUT_QUEUE,msg)
            #send ssh to the instance
            status,stdout,stderr=ssh_the_worker(selected_id)
            logger.debug(stdout)
            logger.debug(stderr)


def ssh_the_worker(instance_id):
    instance = cmd_handler.get_instance(instance_id)
    ssh_client = cmd_handler.ssh_to_instance(instance)
    status,stdout,stderr=cmd_handler.ssh_run_command(ssh_client,"python /home/ubuntu/MyProject/Worker/main.py")
    return (status,stdout,stderr)

def return_users_tasks(user_name,static):
    global LOCAL_QUEUE
    user_dic = LOCAL_QUEUE[user_name]
    #return len(user_dic['Tasks'])
    #add the tasks in user_dic + assigned tasks
    return len(user_dic['Tasks']) + len(static.get_user_tasks(user_name))

def return_all_users():
    global LOCAL_QUEUE
    return LOCAL_QUEUE.keys()

