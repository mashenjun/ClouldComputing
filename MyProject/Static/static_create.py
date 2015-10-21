__author__ = 'mashenjun'
import name_server_start
import static
import Pyro4
from multiprocessing import Process, Value

def create_static_data():
    name_server_start.start_name_server()
    print("1")
    data = static.data_storage()
    ns = Pyro4.locateNS()
    print("2")
    daemon = Pyro4.Daemon()
    print("3")
    data_storage_uri = daemon.register(data)
    ns.register("example.data_storage",data_storage_uri)
    print("4")
    daemon.requestLoop()


if __name__=="__main__":
    p = Process(target = create_static_data, args = ())
    p.start()
    print("add data storage")
