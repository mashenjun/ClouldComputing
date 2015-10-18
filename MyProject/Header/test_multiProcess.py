__author__ = 'mashenjun'
import sys,os.path
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from multiprocessing import Process, Value
import time
import Static.static

def f(n):
    while 1:
        n.value += 1
        print(n.value)
        time.sleep(1)

if __name__ == '__main__':
    p = Process(target=f, args=(static.value,))
    p.start()
