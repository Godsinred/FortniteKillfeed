from __future__ import print_function       #should be on the top
import threading
import time


class MyThread(threading.Thread):
    arr = []
    def run(self):
        print("{} started!".format(self.getName()))              # "Thread-x started!"
        self.arr.append(self.getName())
        time.sleep(10)                                      # Pretend to work for a second
        print(self.arr.pop())
        print("{} finished!".format(self.getName()))             # "Thread-x finished!"

if __name__ == '__main__':
    for x in range(4):                                     # Four times...
        mythread = MyThread(name = "Thread-{}".format(x + 1))  # ...Instantiate a thread and pass a unique ID to it
        mythread.start()                                   # ...Start the thread
        #time.sleep(.9)