import Queue
import threading 
import datetime
import random
import time
from schedulerLogs import *


resourceQueue = Queue.Queue(maxsize=0)


class ThreadResource(threading.Thread):
     """Threaded Resource Processing"""
     def __init__(self, queue,timeSleepMax,responseResourceToGwQueue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._timeSleepMax=timeSleepMax
        self._responseResourceToGwQueue=responseResourceToGwQueue
     def run(self):
        while True:
           msg = self._queue.get()
           logging.info(" Thread resource processing msg  =  %s",msg.getMessage())
           time.sleep(int(random.random()*self._timeSleepMax + 1))
           logging.info(" Thread resource processed msg  =  %s",msg.getMessage())
           msg.completed()
           self._responseResourceToGwQueue.put(msg)
           self._queue.task_done()


class ResourceCounter:
      """Count resources"""
      def __init__(self,resCountMax=1):
          assert isinstance(resCountMax, int) , "ERROR: resCountMax has to be integer"
          self._resCount=resCountMax
          self._maxRes=resCountMax
      def lock(self):
          self._resCount=self._resCount-1
          if self._resCount > -1:
              logging.info("Resources has been decreased to: %s",str(self._resCount))
          else :
             self._resCount=0
             logging.info("Resources has been fully used")
      def release(self):
          self._resCount=self._resCount+1
          if self._resCount < (self._maxRes+1):
             logging.info("Resources has been increased to: %s",str(self._resCount)) 
          else :
             self._resCount=self._maxRes
             logging.info("All Resources are available, Total: %s", str(self._resCount))
      def getResCount(self):
          return self._resCount
