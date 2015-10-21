
from __future__ import print_function
import Pyro4
import name_server_start

class data_storage(object):
    def __init__(self):
        self.idle_list = []
        self.busy_list = []
        self.task = {}

    def get_idle(self):
        return self.idle_list

    def get_busy(self):
        return self.busy_list

    def get_task_value(self,name):
        return self.task[name]

    def get_sum(self):
        return len(self.idle_list)+len(self.busy_list)

    def add_to_idle(self, item):
        if isinstance(item, list):
            self.idle_list.extend(item)
        else:
            self.idle_list.append(item)
        print ("add to idle" + str(self.idle_list))

    def remove_from_idle(self, item):
        self.idle_list.remove(item)
        print ("remove from idle" + str(self.idle_list))

    def add_to_busy(self, item):
        if isinstance(item, list):
            self.busy_list.extend(item)
        else:
            self.busy_list.append(item)
        print ("add to busy" + str(self.busy_list))


    def remove_from_busy(self,item):
        self.busy_list.remove(item)
        print ("remove from busy" + str(self.busy_list))

    def move_to_idle(self,item):
        self.add_to_idle(item)
        self.remove_from_busy(item)
        print ("move to idle" + str(self.idle_list) +str(self.busy_list))

    def move_to_busy(self,item):
        self.add_to_busy(item)
        self.remove_from_idle(item)
        print ("move to busy" + str(self.busy_list) +str(self.idley_list))

    def add_task(self,name):
        self.task[name]+=1
        print ("add_task" + str(self.task) )

    def minus_task(self,name):
        self.task[name]-=1
        print ("minus_task" + str(self.task) )

    def insert_new_task(self, name,num):
        self.task.update({name: num})
        print ("insert_new_task" + str(self.task) )


