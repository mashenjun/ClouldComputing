__author__ = 'mashenjun'
from multiprocessing import Process
import Pyro4

def start():
    Pyro4.naming.startNSloop()

def start_name_server():
    p = Process(target=start, args=())
    p.start()