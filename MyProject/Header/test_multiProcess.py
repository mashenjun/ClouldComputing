__author__ = 'mashenjun'

from multiprocessing import Process, Value
import time
import static

def f(n):
    while 1:
        n.value += 1
        print(n.value)
        time.sleep(1)

if __name__ == '__main__':
    p = Process(target=f, args=(static.value,))
    p.start()
