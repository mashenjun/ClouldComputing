from __future__ import print_function
import threading, sys, os
import name_server_start
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from Logger.custome_logger import get_static_logger,get_trace_worker_wall_time_logger
import Metrix.timemetrix as mt
logger = get_static_logger(__file__)
tracelogger = get_trace_worker_wall_time_logger("tracelogger")
pending_compensate = 0


class data_storage(object):
    def __init__(self):
        self.idle_list = []
        self.busy_list = []
        self.task = {}
        self.details = {}
        self.pending = []
        self.logger_dict = {}
        self.pending_compensate = 0

    def get_idle(self):
        return self.idle_list

    def get_busy(self):
        return self.busy_list

    def get_task_value(self, name):
        return self.task[name]

    def get_task(self):
        return self.task

    def get_idle_num(self):
        return len(self.idle_list)

    def get_sum(self):
        return len(self.idle_list) + len(self.busy_list)

    def get_all_workers_num(self):
        return len(self.pending)+len(self.idle_list) + len(self.busy_list)

    def get_free_worker(self):
        return len(self.idle_list) + len(self.pending)

    def get_pending(self):
        return self.pending

    def get_pending_num(self):
        return len(self.pending)

    def add_to_idle(self, item):
        try:
            if isinstance(item, list):
                self.idle_list.extend(item)
            else:
                self.idle_list.append(item)
            logger.debug("add to idle " + str(self.idle_list))
        except:
            logger.debug("add to idle error" + str(self.idle_list))

    def remove_from_idle(self, item):
        try:
            if isinstance(item, list):
                    self.idle_list = [x for x in self.busy_list if x not in item]
            else:
                    self.idle_list.remove(item)
            logger.debug("remove from idle " + str(self.idle_list))
        except:
            logger.debug("remove from idle error" + str(self.idle_list))

    def add_to_busy(self, item):
        try:
            if isinstance(item, list):
                self.busy_list.extend(item)
            else:
                self.busy_list.append(item)
            logger.debug("add to busy " + str(self.busy_list))
        except:
            logger.debug("add to busy error" + str(self.busy_list))

    def remove_from_busy(self, item):
        try:
            if isinstance(item, list):
                self.busy_list = [x for x in self.busy_list if x not in item]
            else:
                self.busy_list.remove(item)
            logger.debug("remove from busy " + str(self.busy_list))
        except:
            logger.debug("remove from busy error" + str(self.busy_list))

    def move_to_idle(self, item):
        if item in self.busy_list:
            self.add_to_idle(item)
            self.remove_from_busy(item)
        else:
            logger.debug("can not move to idle")


    def move_to_busy(self, item):
        if item in self.idle_list:
            self.add_to_busy(item)
            self.remove_from_idle(item)
        else:
            logger.debug("can not move to busy")

    def add_task(self, name):
        self.task[name] += 1
        logger.debug("add_task " + str(self.task))


    def minus_task(self, name):
        self.task[name] -= 1
        logger.debug("minus_task " + str(self.task))

    def insert_new_task(self, name, num):
        original = 0
        if self.task.has_key(name):
            original = self.task[name]
        self.task[name] = original + num
        # self.task.update({name: num})
        logger.debug("insert_new_task " + str(self.task[name]))

    def del_task(self, name):
        self.task.pop(name)
        logger.debug("remove_task " + str(self.task))

    def get_all_tasks(self):
        return self.details

    def get_user_tasks(self, name):
        return {k: v for k, v in self.details.items() if v.split('/')[0] == name}

    def register_in_details(self, msg, instance_id):
        # structure of details {instance_id:new_file}, invoke by worker
        self.details[instance_id] = msg
        logger.debug("add to details " + str(self.details))
        #--------------------this is for logger time------------
        self.logger_dict[instance_id] = msg
        return self.details

    def de_register_in_details(self, instance_id):
        try:
            return_msg = self.details.pop(instance_id, None)
            logger.debug("return_msg "+ str(instance_id)+" with "+str(return_msg))
            logger.debug("details is "+ str(self.details))
            return return_msg
        except KeyError:
            logger.debug("error details is "+ str(self.details))

    def add_pending(self,instancied):
        try:
            if isinstance(instancied, list):
                self.pending.extend(instancied)
            else:
                self.pending.append(instancied)
            logger.debug("add pending "+ str(self.pending))
        except:
            logger.debug("add pending error"+ str(self.pending))

    def remove_pending(self,instancied):
        try:
            self.pending.remove(instancied)
            logger.debug("remove pending " + str(self.pending))
        except:
            logger.debug("remove pending error" + str(self.pending))

    def move_from_pending_to_idle(self,instanceid):
        self.remove_pending(instanceid)
        self.add_to_idle(instanceid)

    def move_from_idle_to_pending(self,instanceid):
        self.remove_from_idle(instanceid)
        self.add_pending(instanceid)

    def get_figName_from_logger_dict(self,instanceId):
        return self.logger_dict[instanceId]

    def add_pending_compensate(self,num):
        self.pending_compensate += num
        return self.pending_compensate

    def decrease_pending_compensate(self):
        self.pending_compensate -= 8
        return self.pending_compensate

    def reset_pending_compensate(self):
        self.pending_compensate = 0
        return self.pending_compensate