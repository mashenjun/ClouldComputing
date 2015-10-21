__author__ = 'mashenjun'
from multiprocessing import Process
import Pyro4

def create():
    Pyro4.naming.startNSloop(host="192.168.174.134",port=9999)

def start_name_server():
    p = Process(target=create, args=())
    p.start()