import Queue
import random
import string
import threading
import datetime
import time
from message import Message
from generalQueue import GeneralQueue
from schedulerLogs import *


msgForwarderQueue=Queue.PriorityQueue(maxsize=0)

class ThreadForwarderToGwIntf(threading.Thread):
    """Threaded Forwarder to GW INTF """
    def __init__(self, queue, resourceCounter,gwIntf):
        threading.Thread.__init__(self)
        self._queue = queue
        self._resourceCounter=resourceCounter
        self._gwIntf=gwIntf
    def run(self):
        while True:
           if self._resourceCounter.getResCount() > 0:
               if self._queue.empty():
                   logging.info("Thread Forwarder Queue is empty")
                   time.sleep(0.2)
               else:
                   msg = self._queue.get()
                   self._gwIntf.send(msg[1])
                   self._resourceCounter.lock()
                   logging.info("Thread Forwarder send msg = %s to GW INTF ",msg[1].getMessage())
                   self._queue.task_done()
