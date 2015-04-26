import Queue
import threading
import datetime
import random
import time
from generalQueue import GeneralQueue
from MessageGenerator import fillMsgGeneratorQueue, MessageGenerator, ThreadMessageGeneratorSender, msgGeneratorQueue
from message import Message
from resources import  resourceQueue
from gwInterface import gwInterface, ThreadGwSenderToResource, gwQueue
from ResourceScheduler import ThreadForwarderToGwIntf, msgForwarderQueue
from resources import ResourceCounter, ThreadResource,resourceQueue
from responding import ThreadResponseResourceToGw, responseResourceToGwQueue
from Rules import ThreadRule, msgRuleQueue, Rule
from config import maxStep,maxBurstSize,msgGroupIdRange,timeSleepMaxGenerator,numberResources,ruleId, priorityGroupList, modulo, remainderList,timeSleepMaxResource 

def main():
    fillMsgGeneratorQueue(maxStep=maxStep,maxBurstSize=maxBurstSize,msgGroupIdRange=msgGroupIdRange)
    Gw=gwInterface()
    Resource=ResourceCounter(numberResources)
    #basicRule1=Rule(ruleId=1,priorityGroupList=[])
    #basicRule2=Rule(ruleId=2,priorityGroupList=[3,1])
    #basicRule3=Rule(ruleId=3,modulo=[3],remainderList=[0,1])
    cancelationRule=Rule()     #Rule(ruleId=4, cancelation=[2])
    terminationRule=Rule()     #Rule(ruleId=5,termination=[3])
    
    if ruleId==1:
        basicRule=Rule(ruleId=ruleId,priorityGroupList=[])
    if ruleId==2:
        basicRule=Rule(ruleId=ruleId,priorityGroupList=priorityGroupList)
    if ruleId==3:
        basicRule=Rule(ruleId=ruleId,modulo=modulo,remainderList=remainderList)

    t = ThreadMessageGeneratorSender(msgGeneratorQueue,msgRuleQueue,timeSleepMaxGenerator)

    t1=ThreadRule(msgRuleQueue,msgForwarderQueue,Resource,rule=basicRule,ruleCancelation=cancelationRule,ruleTermination=terminationRule)

    t2=ThreadForwarderToGwIntf(msgForwarderQueue,Resource,Gw)

    t3=ThreadGwSenderToResource(gwQueue,resourceQueue)

    t4=ThreadResource(resourceQueue,timeSleepMaxResource,responseResourceToGwQueue)
    
    t5=ThreadResponseResourceToGw(responseResourceToGwQueue,Resource)


    t.setDaemon(True)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
    t5.setDaemon(True)
    t.start()
    t1.start()
    t2.start()
    t3.start()    
    t4.start()
    t5.start()


 
    main_thread=threading.currentThread()
    threads=threading.enumerate()
    for t in threads:
        print t
    msgGeneratorQueue.join()
    msgRuleQueue.join()
    msgForwarderQueue.join()
    gwQueue.join()
    resourceQueue.join()
    responseResourceToGwQueue.join()

main()
