__author__ = 'mashenjun'
import Pyro4
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger.custome_logger import get_logger
from configFile.instanceConfig import Config
from SQS import handler as SQS_handler
from EC2 import cmdshell as cmd_handler
import deadline

config = Config()
logger = get_logger(__file__)
INPUT_QUEUE = config.ConfigSectionMap()["sqs_input_queue"]

LOCAL_QUEUE = {}
static = Pyro4.Proxy("PYRONAME:example.data_storage@192.168.174.134:9999")
KEY_PATH = config.ConfigSectionMap()["path_to_key"]

def insert_new_job(new_files):
    map(insert_single_job,new_files)
    #refresh the task queue
    for user in return_all_users():
        static.insert_new_task(user,return_users_tasks(user))
        LOCAL_QUEUE[user]['Deadline'] = deadline.deadline(LOCAL_QUEUE[user]['Counter'])
    print "the task dict is: "
    print static.get_task()
    #result = [insert_new_job(p, p) for p in new_files]

def insert_single_job(file):
    global LOCAL_QUEUE
    user_name = file.split('/')[0]
    if (not LOCAL_QUEUE.has_key(user_name)):
        LOCAL_QUEUE[user_name]={'Tasks':[],'Counter':0}

    user_dic = LOCAL_QUEUE[user_name]
    user_dic['Tasks'].append(file)
    user_dic['Counter']+=2

def return_task():
    global LOCAL_QUEUE
    user_list = sorted(LOCAL_QUEUE.keys(),key = lambda e:LOCAL_QUEUE[e]["Deadline"].num)
    logger.debug(user_list)
    if len(user_list) ==0:
        return None
    else:
        user_tasks = LOCAL_QUEUE[user_list[0]]['Tasks']
        if len(user_tasks) >1:
            return user_tasks.pop(0)
        elif len(user_tasks) == 1:
            user_dict = LOCAL_QUEUE.pop(user_list[0],None)
            user_deadline = user_dict['Deadline']
            user_deadline.valid = 0
            user_tasks = user_dict['Tasks']
            return user_tasks.pop(0)
        else :
            return None

def send_message_to_sqs(sqs):
    # get the length of idle list
    num_idle = len(static.get_idle())
    logger.debug(num_idle)
    #header_IP = EC2_handler.get_local_ipv4()
    header_IP ="192.168.174.134"
    # iterate the idle and assign the jobs to the idle worker until there are no tasks in local queue or no workers
    for i in range(0,num_idle):
        selected_job = return_task()
        logger.debug(selected_job)
        if selected_job is None:
            break
        else:
            selected_id=static.get_idle()[0]
            #move the instance to busy list
            static.move_to_busy(selected_id)
            #ssh to that id
            cmd_handler.get_instance(selected_id)
            #build the msg username/filename#header_IP
            msg = selected_job +"#"+header_IP
            #send msg to invoke the instance
            SQS_handler.create_msg(sqs,INPUT_QUEUE,msg)
            #send ssh to the instance
            status,stdout,stderr=ssh_the_worker(selected_id)


def ssh_the_worker(instance_id):
    instance = cmd_handler.get_instance(instance_id)
    ssh_client = cmd_handler.ssh_to_instance(instance)
    status,stdout,stderr=cmd_handler.ssh_run_command(ssh_client,"python /home/ubuntu/MyProject/Worker/main.py")
    return (status,stdout,stderr)

def return_users_tasks(user_name):
    global LOCAL_QUEUE
    user_dic = LOCAL_QUEUE[user_name]
    return len(user_dic['Tasks'])

def return_all_users():
    global LOCAL_QUEUE
    return LOCAL_QUEUE.keys()