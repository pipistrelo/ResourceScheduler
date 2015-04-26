import Queue
import random
import string
import threading 
import datetime
import time
from message import Message
from generalQueue import GeneralQueue
from schedulerLogs import *

msgGeneratorQueue = Queue.Queue(maxsize=0)

def fillMsgGeneratorQueue(maxStep=100,maxBurstSize=5,msgGroupIdRange=3):
    assert isinstance(maxBurstSize,int) , "ERROR: maxBurstSize has to be inetger"
    assert maxBurstSize  > 0 , "ERROR: maxBurstSize has to be positive integer"
    assert isinstance(maxStep,int) , "ERROR: maxStep has to be inetger"
    assert maxStep  > 0 , "ERROR: maxStep has to be positive integer"
    assert isinstance(msgGroupIdRange, int) , "ERROR: msgGroupIdRange has to be integer"
    assert msgGroupIdRange > 0  , "ERROR: msgGroupIdRange has to be positive integer"
   
    ## queue item defines a burst size for each generetion step
    if msgGeneratorQueue.empty():
        for j in range(maxStep):
            msgGeneratorQueue.put([random.randint(1,maxBurstSize),random.randint(1,msgGroupIdRange)])


class MessageGenerator:


    ## @param msgRef is message unique reference
    ## @param msgGroupId is group id in which message belongs
    ## @param msgBody is body of message
    ## @param msgsState is the state of message <created|wait|completed> created is used when message is created, wait when message is being processed, completed when message
    ## has already been processed
    def __init__(self,msgBurstSize=1, msgGroupIdRange=1):
        assert isinstance(msgGroupIdRange, int) , "ERROR: msgGroupIdRange has to be integer"
        assert msgGroupIdRange > 0  , "ERROR: msgGroupIdRange has to be positive integer"
        assert isinstance(msgBurstSize,int) , "ERROR: msgBurstSize has to be inetger"
        assert msgBurstSize > 0 , "ERROR: msgBurstSize has to be positive integer"
        self._msgGroupIdRange=msgGroupIdRange
        self._msgBurstSize=msgBurstSize
        
        
    def generateMsgs(self): 
        msgGeneratedList=[]
        for i in range(self._msgBurstSize):
            digits = "".join( [random.choice(string.digits) for j in xrange(5)] )
            chars = "".join( [random.choice(string.letters) for j in xrange(5)] )
            msgBody=digits + chars
            msgGroupId=int(random.random()*self._msgGroupIdRange + 1)
            try :
                msg=Message(msgRef=msgBody,msgGroupId=msgGroupId,msgBody=msgBody)
                msgGeneratedList.append(msg)
            except :
                logging.error("Error with Message class")
        return msgGeneratedList


class ThreadMessageGeneratorSender(threading.Thread):
     """Threaded Message generator, client side of msg generator"""
     def __init__(self, queue=None,msgRuleQueue=None,timeSleepMax=1):
        threading.Thread.__init__(self)
        self._queue = queue
        self._msgRuleQueue=msgRuleQueue
        self._timeSleepMax=timeSleepMax
     def run(self):
        while True:
           item=self._queue.get() 
           try:
               maxBurstSize=item[0]
               msgGroupIdRange=item[1]
               msgGenerator=MessageGenerator(msgBurstSize=maxBurstSize,msgGroupIdRange=msgGroupIdRange)
               msgList=msgGenerator.generateMsgs()
           except :
               logging.error("Error with Messagegenerator class")

           for m in msgList:
               #self._msgForwarderQueue.put(m)
               self._msgRuleQueue.put(m)
               logging.info("ThreadMessageGeneratorSender Genarated msg %s",m.getMessage())

           self._queue.task_done()

           # Messages are produced with random time scheduling
           time.sleep(int(random.random()*self._timeSleepMax + 1))

