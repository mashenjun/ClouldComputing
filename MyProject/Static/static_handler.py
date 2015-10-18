
from __future__ import print_function
import sys
import Pyro4
# may be over lap
class Person(object):
    def __init__(self, name):
        self.name = name

    def get_idle(self, static):
        return static.get_idle()

    def add_idle(self, static,):
        item = input("Type a thing you want to store (or empty): ").strip()
        static.add_to_idle(self.name, item)

    def remove_idle(self, static,):
        item = input("Type something you want to take (or empty): ").strip()
        static.remove_from_idle(self.name, item)


# test
#uri = input("Enter the uri of the warehouse: ").strip()
def main():
    static = Pyro4.Proxy("PYRONAME:example.data_storage")
    janet = Person("Janet")
    janet.add_idle(static)
    print(janet.get_idle(static))

if __name__=="__main__":
    main()
