import Queue
import threading
import datetime
import random
import time
from message import Message
from schedulerLogs import *

cliSendMsgQueue = Queue.Queue(maxsize=0)


class ThreadCliSendMsgToRule(threading.Thread):
     """Threaded Cli Sender To Rule in order to send cancelation, termination or update rule messages
         groupId shold be set to value -1 for these messages
         # termination : body example of messages :  { "termination":[2,3]}, or { "termination":[3]}, or { "termination":[]}
           msg shoudl be defined the following way : Message(msgRef="1a",msgGroupId=-1,msgBody='{"termination":[2,3]}')
         # rule update : example of msg body { "updateRule":2, "priorityGroupList":[2,4]}, {"updateRule":3, "modulo":[2],"remainderList":[1] }
           {"updateRule":1}
         # cancelation : exmaple of msg body  { "cancelation":[2,3]}, or { "cancelation":[3]}
           the first  means that group id 2,3 should be cancelled
           the second means that group id 2 should be processed again and only 3 should be cancelled further
           { "cancelation":[]} means that all group shoudl be processed further in normal way with given rule
     """
     def __init__(self, queue,msgRuleQueue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._msgRuleQueue=msgRuleQueue
     def run(self):
        while True:
           msg = self._queue.get()
           self._msgRuleQueue.put(msg)
           logging.info("Thread CLI  Send Msg to Rule msg =[  %s ] to Rule Queue",msg.getMessage())
           self._queue.task_done()
