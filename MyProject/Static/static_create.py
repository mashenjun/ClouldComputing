__author__ = 'mashenjun'
import name_server_start
import static
import Pyro4
def create_static_data():
    name_server_start.start_name_server()
    data = static.data_storage()
    daemon = Pyro4.Daemon()
    data_storage_uri = daemon.register(data)
    ns = Pyro4.locateNS()
    ns.register("example.data_storage",data_storage_uri)
    print("add data storage")
    daemon.requestLoop()

