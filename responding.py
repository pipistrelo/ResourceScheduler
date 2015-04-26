import Queue
import threading
import datetime
import random
import time
from schedulerLogs import *


responseResourceToGwQueue = Queue.Queue(maxsize=0)


class ThreadResponseResourceToGw(threading.Thread):
     """Threaded Resource Processing"""
     def __init__(self, queue,resCounter):
        threading.Thread.__init__(self)
        self._queue = queue
        self._resCounter=resCounter
     def run(self):
        while True:
           msg = self._queue.get()
           self._resCounter.release()
           logging.info("Thread Response Resource to GW release resource for msg  = %s",msg.getMessage())
           self._queue.task_done()
