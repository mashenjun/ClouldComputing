
from __future__ import print_function
import Pyro4
import name_server_start

class data_storage(object):
    def __init__(self):
        self.idle_list = []
        self.busy_list = []
        

    def get_idle(self):
        return self.idle_list

    def get_busy(self):
        return self.idle_list

    def get_sum(self):
        return len(self.idle_list)+len(self.busy_list)

    def add_to_idle(self, name, item):
        self.idle_list.append(item)
        print ("add" + str(len(self.idle_list)))

    def remove_from_idle(self, name ,item):
        self.idle_list.remove(item)
        print ("remove" + str(len(self.idle_list)))

    def add_to_busy(self, name, item):
        self.idle_list.append(item)
        print ("add" + str(len(self.idle_list)))

    def remove_from_busy(self, name ,item):
        self.idle_list.remove(item)
        print ("remove" + str(len(self.idle_list)))
