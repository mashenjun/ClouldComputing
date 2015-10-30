__author__ = 'mashenjun'
from EC2 import handler as EC2_handler

import threading
import Pyro4



class thread(threading.Thread):
    def __init__(self, t, *args):
        threading.Thread.__init__(self, target=t, args=args)
        self.start()

def update_static(msg,Head_location):
    my_instanceId = EC2_handler.get_local_instanceId()
    print(Head_location)
    static = Pyro4.Proxy("PYRONAME:example.data_storage@"+Head_location)
    static.register_in_details( msg,my_instanceId)

def del_static(Head_location):
    my_instanceId = EC2_handler.get_local_instanceId()
    static = Pyro4.Proxy("PYRONAME:example.data_storage@"+Head_location)
    static.de_register_in_details(my_instanceId)



def start_update_static(msg,Head_location):
    #start the thread
    thread(update_static,msg,Head_location)

def start_del_static(Head_location):
    thread(del_static,Head_location)