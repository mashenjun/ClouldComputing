__author__ = 'mashenjun'
import sys,os.path
import threading
import time
import static
sys.path.insert(1, os.path.join(sys.path[0], '..'))


exitFlag = 0

data = 0;

def listening(threadName, delay):
    while True:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        static.set(static.get())
        print(static.get())

class myThread (threading.Thread):
    def __init__(self, threadID, name,):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def runs(self):
        listening(self.name, 2)

def main():
    # Create new threads
    thread1 = myThread(1, "Thread-1")
    # Start new Threads
    thread1.start()
    print "Exiting Main Thread"

if __name__ == "__main__":
    main()