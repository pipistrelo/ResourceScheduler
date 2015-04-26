import Queue
import threading
import datetime
import random
import time
from message import Message
from schedulerLogs import *

gwQueue = Queue.Queue(maxsize=0)

class gwInterface:
     """GW Interface"""
     def __init__(self):
         pass
         #print "GW Interface Init"
     def send(self,msg):
         msg.updateMsgState("sent")
         gwQueue.put(msg)



class ThreadGwSenderToResource(threading.Thread):
     """Threaded GW Sender To Resource"""
     def __init__(self, queue,resourceQueue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._resourceQueue=resourceQueue
     def run(self):
        while True:
           msg = self._queue.get()
           self._resourceQueue.put(msg)
           now = datetime.datetime.now()
           logging.info("Thread GW send msg = %s to resource",msg.getMessage())
           self._queue.task_done()
