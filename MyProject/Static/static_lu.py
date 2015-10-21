
from __future__ import print_function
import Pyro4
import name_server_start

class data_storage(object):
    def __init__(self):
        self.idle_list = []
        self.busy_list = []
        self.task = {}
        self.details = {}

    def get_idle(self):
        return self.idle_list

    def get_busy(self):
        return self.idle_list

    def get_task_value(self,name):
        return self.task[name]
        
    def get_all_tasks(self):
        return self.details
        
    def get_user_tasks(self,name):
        return self.details[name]

    def get_sum(self):
        return len(self.idle_list)+len(self.busy_list)
        
    def check_user_exist(self,name):
        return self.details.has_key(name)
        
    def add_task_in_dict(self,new_file,instance_id):
        user_name = new_file.split('/')[0]
        file_name = new_file.split('/')[1]            
        #if there is already this user in the dict        
        if(not self.check_user_exist(user_name)):
            self.details[user_name]={}
        user_dict = self.details[user_name]
        user_dict[file_name]=instance_id
        return self.details
        
    def delete_task_in_dict(self,new_file,instance_id):
        user_name = new_file.split('/')[0]
        file_name = new_file.split('/')[1]  
        user_dict = self.details[user_name]
        del user_dict[file_name]
        return self.details

    def add_to_idle(self,item):
        self.idle_list.append(item)
        #print ("add" + str(len(self.idle_list)))

    def remove_from_idle(self,item):
        self.idle_list.remove(item)
        #print ("remove" + str(len(self.idle_list)))

    def add_to_busy(self,item):
        self.idle_list.append(item)
        #print ("add" + str(len(self.idle_list)))

    def remove_from_busy(self,item):
        self.idle_list.remove(item)
        #print ("remove" + str(len(self.idle_list)))

    def move_to_idle(self,item):
        self.add_to_idle(item)
        self.remove_from_busy(item)

    def move_to_busy(self,item):
        self.add_to_busy(item)
        self.remove_from_idle(item)

    def add_task(self,name):
        self.task[name]+=1

    def minus_task(self,name):
        self.task[name]-=1

    def insert_new_task(self, name,num):
        self.task.update({name: num})


