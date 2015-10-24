__author__ = 'mashenjun'
from multiprocessing import Process
import Pyro4

def create():
    Pyro4.naming.startNSloop(host="172.31.30.52",port=9999)

def start_name_server():
    p = Process(target=create, args=())
    p.start()