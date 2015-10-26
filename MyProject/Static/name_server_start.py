__author__ = 'mashenjun'
from multiprocessing import Process
import Pyro4
import sys,os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from configFile.instanceConfig import Config

config = Config()
ip = config.ConfigSectionMap()['head_ip']

def create():
    Pyro4.naming.startNSloop(host=ip,port=9999)

def start_name_server():
    p = Process(target=create, args=())
    p.start()