__author__ = 'yun'


global picNum
picNum = {"yunlu45":45,"yunlu30":30,"yunlu15":15}

global startTime_dict_process_time
startTime_dict_process_time = {}

global startTime_dict_wall_time
startTime_dict_wall_time = {}

global start_allocate_dict_process_time
start_allocate_dict_process_time = {}

global start_allocate_dict_wall_time
start_allocate_dict_wall_time = {}

global launch_new_instance_process_time
launch_new_instance_process_time = {}

global launch_new_instance_wall_time
launch_new_instance_wall_time = {}

global send_file_2queue_process_time
send_file_2queue_process_time = {}

global send_file_2queue_wall_time
send_file_2queue_wall_time = {}

global setup_start_process_time
setup_start_process_time = 0

global setup_start_wall_time
setup_start_wall_time = 0


def cal_workers_life_process_time(end,num):
    return (end-setup_start_process_time)*num - sum(launch_new_instance_process_time.values())

def cal_workers_life_wall_time(end,num):
    return (end-setup_start_wall_time)*num - sum(launch_new_instance_wall_time.values())


def append_time_in_dict_process(user,num):
    if not start_allocate_dict_process_time.has_key(user):
        start_allocate_dict_process_time[user] = []
    start_allocate_dict_process_time[user].append(num)

def append_time_in_dict_wall(user,num):
    if not start_allocate_dict_wall_time.has_key(user):
        start_allocate_dict_wall_time[user] = []
    start_allocate_dict_wall_time[user].append(num)


