__author__ = 'mashenjun'
import time
import threading

class deadline(object):
    num = 0
    valid = 1
    def __init__(self, time):
        self.num = time
        t=threading.Thread(target= self.countdown)
        t.start()

    def countdown(self):
        while ( self.num > 0):
            self.num -= 1
            time.sleep(1)
            if self.valid == 0:
                break
        if (self.num == 0) :
            #launch a new instance



    def add_num(self, value):
        self.num +=value


