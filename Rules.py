import json
import Queue
import string
import threading
import datetime
import time
from message import Message
from schedulerLogs import *


class Rule(object):
    
    ## @param ruleId is defined which prioritisation rule is being used
    ## ruleId=1 this rule prioritise messages from groups already started 
    ## ruleId=2 this rule prioritise messages from groups in priorityGroupList
    ## ruleId=3 this rule prioritise messages from groups that have groupId which modulo gives remainder in remainderList
    ## ruleId=4 this rule is design for cancelation type messages where in cancelation list consists of a list of group id that a processing should be cancelled
    ## ruleId=5 this rule is design for termination type messages where in termination list consists of a list of group id that should be terminated with error msg
    ## @param kwargs is dictionary in which are expected these keys priorityGroupList | remainderList | modulo | cancelation | termination
    ## 
    def __init__(self,**kwargs):
        for k in ["ruleId","priorityGroupList", "remainderList", "modulo", "cancelation","termination"]:
            self.__setattr__(k, None)
        for k in kwargs.keys():
             if k in ["ruleId","priorityGroupList", "remainderList", "modulo", "cancelation","termination"]:
                 if k=="ruleId":
                    assert isinstance(kwargs[k],int) , "{0}  key value has to be a integer".format(k)
                 else :
                    assert isinstance(kwargs[k],list) , "{0}  key value has to be a list of integers".format(k)
                    for i in kwargs[k]:
                       assert isinstance(i,int) , "{0}  key value has to be a integer".format(k)
                    if k=="modulo":
                       assert len(kwargs[k])==1 , "{0}  key value has to be a one integer".format(k)
                       assert kwargs[k][0] > 0 and isinstance(kwargs[k][0],int), "{0}  key value has to be an integer".format(k)
                       
                 self.__setattr__(k, kwargs[k])
   
    def setParam(self,**kwargs):
        for k in kwargs.keys():
             if k in ["ruleId","priorityGroupList", "remainderList", "modulo", "cancelation","termination"]:
                 if k=="ruleId":
                     assert isinstance(kwargs[k],int) , "{0}  key value has to be a integer".format(k)
                 else :
                     assert isinstance(kwargs[k],list) , "{0}  key value has to be a list of integers".format(k)
                     for i in kwargs[k]:
                       assert isinstance(i,int) , "{0}  key value has to be a integer".format(k)
                     if k=="modulo":
                       assert len(kwargs[k])==1 , "{0}  key value has to be a one integer".format(k)
                       assert kwargs[k][0] > 0 and isinstance(kwargs[k][0],int), "{0}  key value has to be an integer".format(k)
                 self.__setattr__(k, kwargs[k])

    def getParam(self,param):
        if param in ["ruleId","priorityGroupList", "remainderList", "modulo", "cancelation","termination"]:
            l=["self",param]
            return eval('.'.join(l))

    def run(self,msg):
        if  self.ruleId==1:
            if msg.getMsgGroupId() in self.priorityGroupList:
                logging.info("Priority Rule [ %s ] : Priority of the first comming msg to GW and given group id is present in Priority Group List is [ %s ]:  MSG: [ %s ] and Priority:[ %s ] has higher priority",self.ruleId,self.priorityGroupList,msg.getMessage(),1)
                return 1
            else:
                logging.info("Priority Rule [ %s ]  : Priority of the first comming msg to GW and given group id is not present in Priority Group List is [ %s ]:  MSG: [ %s ] and Priority:[ %s ] has lower priority",self.ruleId,self.priorityGroupList,msg.getMessage(),2)
                return 2

        if self.ruleId==2:
            if self.priorityGroupList:
                if msg.getMsgGroupId() in self.priorityGroupList:
                    logging.info("Priority Rule [ %s ] : Prioritising the group ids in the Group Priority List [ %s ] : MSG: [ %s ] and Priority: [ %s ] has higher priority",self.ruleId,self.priorityGroupList,msg.getMessage(),1) 
                    return 1
                else :
                    logging.info("Priority Rule [ %s ] : the group id  is not in  the Group Priority List the Group Priority List [ %s ] : MSG:[ %s ] and Priority:[ %s ] has lower priority",self.ruleId,self.priorityGroupList,msg.getMessage(),2)
                    return 2
            else:
                logging.error("Priority Rule [ %s ]: Group Priority List is empty [ %s ] : MSG:[ %s ] and Priority:[ %s ] has  lower priority",self.ruleId,self.priorityGroupList,msg.getMessage(),3)
                return 3

        if self.ruleId==3:
            if (self.remainderList and self.modulo):
                remain=int(msg.getMsgGroupId()) % int(self.modulo[0])
                if remain  in self.remainderList : 
                    logging.info("Priority Rule [ %s ]: Prioritising the group ids that gives by  modulo [ %s ]  reaminder that is  in Remainder Priority List [ %s ] :  MSG:[ %s ] and Priority: [ %s ] has higher priority",self.ruleId,self.modulo[0],self.remainderList,msg.getMessage(),1)
                    return 1
                else :
                    logging.info("Priority Rule [ %s ] : Group id does not give by modulo [  %s ]  the remainder that is in Remainder Priority List [ %s ] :  MSG:[ %s ] and Priority: [ %s ] has lower priority",self.ruleId,self.modulo[0],self.remainderList,msg.getMessage(),2)
                    return 2
            else :
                    logging.error("Priority Rule [ %s ] : modulo number [ %s ] or  Remainder Priority List [ %s ]  has value None or both : MSG: [ %s  ] and Priority: [ %s ] has  lower priority",self.ruleId,self.modulo[0],self.remainderList,msg.getMessage(),3)
                    return 3 

        if self.ruleId==4:
            if msg.getMsgGroupId() in self.cancelation : 
                logging.info("Cancelation Rule [ %s ] : Cancel processing all messages with group id presents in cancelation list [ %s ] : Cancelled processing of  MSG:[ %s ] and Priority: [ %s ]", self.ruleId,self.cancelation,msg.getMessage(),4)
                return 4 
            else:
                return 1

        
        if self.ruleId==5:
            if msg.getMsgGroupId() in self.termination :
                logging.info("Termination Rule [ %s ] : Terminate all messages with group id presents in Termination group list [ %s ] : Terminate processing of  MSG: [ %s ] and Priority: [ %s ]", self.ruleId,self.termination,msg.getMessage(),5)
                return 5
            else :
                return 1        




msgRuleQueue = Queue.Queue(maxsize=0)


class ThreadRule(threading.Thread):
     """Threaded Rule assigns priority to each message according to applied rule and send msg to forwarder queue
        rule is basic rule 1,2,or 3
        ruleCancelation and rule Termination are special rules
        ruleUpdate msg is to update basci rule 1,2,or 3 """
     def __init__(self, queue=None,msgForwarderQueue=None,resourceCounter=None,rule=None,ruleCancelation=None,ruleTermination=None):
        threading.Thread.__init__(self)
        self._queue = queue
        self._msgForwarderQueue=msgForwarderQueue
        self._resourceCounter=resourceCounter
        self._rule=rule
        self._ruleCancelation=ruleCancelation
        self._ruleTermination=ruleTermination
        self._ruleUpdateCounter=0
        self._msgWaittingQueue=Queue.PriorityQueue(maxsize=0)
     def run(self):
        while True:
           while self._queue.empty():
               #logging.info("ThreadRule Rule Queue is empty")
               while (self._msgForwarderQueue.qsize() < self._resourceCounter.getResCount()) and (not self._msgWaittingQueue.empty()):
                       getMsg=self._msgWaittingQueue.get()
                       # in the case of rule id when all msg prioritised group id has been processed in current waitting queue
                       # the first group id from lower priority group becomes priority group id and rerule all msgs in waitting queue
                       if getMsg[0]==2 and self._rule.getParam("ruleId")==1:
                          self._rule.setParam(ruleId=1,priorityGroupList=[getMsg[1].getMsgGroupId()])
                          logging.info("ThreadRule Priority Rule 1, Start reruling waitting queue msgs with Priority Group List [ %s ]",self._rule.getParam("priorityGroupList"))
                          helpQueue=Queue.PriorityQueue(maxsize=0)
                          while (not self._msgWaittingQueue.empty()):
                              m=self._msgWaittingQueue.get()
                              reruleMsgPriority=self._rule.run(m[1])
                              reruleMsg=(reruleMsgPriority,m[1])
                              helpQueue.put(reruleMsg)
                          while (not helpQueue.empty()):
                              self._msgWaittingQueue.put(helpQueue.get())
                          logging.info("ThreadRule Priority Rule 1,Finish reruling waitting queue msgs with Priority Group List [ %s ]",self._rule.getParam("priorityGroupList"))

                       self._msgForwarderQueue.put(getMsg)
                       logging.info("ThreadRule send msg to forwarder Queue with priority [ %s ] and  msg [%s]",getMsg[0],getMsg[1].getMessage())
                       logging.info("ThreadRule msg waittingqueue has size [ %s ] ",self._msgWaittingQueue.qsize()) 
           msg=self._queue.get()
           if msg.getMsgGroupId() > 0 :
               # group id is numbered like 1,2,3,...
               if self._ruleUpdateCounter > 0 :
                   logging.info("ThreadRule ruleUpdateCounter value is [ %s ]", self._ruleUpdateCounter)
                   if (self._rule.getParam("ruleId")==1) and (len(self._rule.getParam("priorityGroupList"))==0):
                       self._rule.setParam(priorityGroupList=[msg.getMsgGroupId()])
                   logging.info("ThreadRule Priority Rule [ %s ], Start reruling waitting queue msgs",self._rule.getParam("ruleId"))
                   helpQueue=Queue.PriorityQueue(maxsize=0)
                   while (not self._msgWaittingQueue.empty()):
                       m=self._msgWaittingQueue.get()
                       reruleMsgPriority=self._rule.run(m[1])
                       reruleMsg=(reruleMsgPriority,m[1])
                       helpQueue.put(reruleMsg)
                   while (not helpQueue.empty()):
                       self._msgWaittingQueue.put(helpQueue.get())
                   logging.info("ThreadRule Priority Rule [ %s ], Finish reruling waitting queue msgs",self._rule.getParam("ruleId"))
                   self._ruleUpdateCounter-=1
                   logging.info("ThreadRule ruleUpdateCounter value is [ %s ]", self._ruleUpdateCounter)
               else:
                   if (self._rule.getParam("ruleId")==1) and (len(self._rule.getParam("priorityGroupList"))==0):
                       self._rule.setParam(priorityGroupList=[msg.getMsgGroupId()])
                       logging.info("ThreadRule Priority Rule 1, Set Priority Group List [ %s ]",self._rule.getParam("priorityGroupList"))

                   priorityMsgRule=self._rule.run(msg)
                   priorityMsg=(priorityMsgRule,msg)
                   if self._ruleCancelation.getParam("ruleId") is not None:
                       priorityMsgCancelation=self._ruleCancelation.run(msg)
                       priorityMsg=(priorityMsgCancelation,msg)
                   if self._ruleTermination.getParam("ruleId") is not None:
                       priorityMsgTermination=self._ruleTermination.run(msg)
                       if (priorityMsgCancelation==4 or priorityMsgCancelation==1) and priorityMsgTermination==5:
                           # cancelation is overwritten by termination
                           priorityMsg=(5,msg)
                       if (priorityMsgCancelation==4 and priorityMsgTermination==1):
                           priorityMsg=(4,msg)
                   if priorityMsg[0]!=4 or priorityMsg[0]!=5: 
                       self._msgWaittingQueue.put(priorityMsg)
                   else :
                       if priorityMsg[0]==4:
                          logging.info("ThreadRule priority [%s] and  msg [%s] has been cancelled",priorityMsg[0],priorityMsg[1].getMessage())
                       if priorityMsg[0]==5:
                          logging.error("ThreadRule priority [%s] and  msg [%s] has been terminated",priorityMsg[0],priorityMsg[1].getMessage())
                   while (self._msgForwarderQueue.qsize() < self._resourceCounter.getResCount()) and (not self._msgWaittingQueue.empty()):
                       getMsg=self._msgWaittingQueue.get()
                       # in the case of rule id when all msg prioritised group id has been processed in current waitting queue
                       # the first group id from lower priority group becomes priority group id and rerule all msgs in waitting queue
                       if getMsg[0]==2 and self._rule.getParam("ruleId")==1:
                          self._rule.setParam(ruleId=1,priorityGroupList=[getMsg[1].getMsgGroupId()])
                          logging.info("ThreadRule Priority Rule 1, Start reruling waitting queue msgs with Priority Group List [ %s ]",self._rule.getParam("priorityGroupList"))
                          helpQueue=Queue.PriorityQueue(maxsize=0)
                          while (not self._msgWaittingQueue.empty()):
                              m=self._msgWaittingQueue.get()
                              reruleMsgPriority=self._rule.run(m[1])
                              reruleMsg=(reruleMsgPriority,m[1])
                              helpQueue.put(reruleMsg)
                          while (not helpQueue.empty()):
                              self._msgWaittingQueue.put(helpQueue.get())
                          logging.info("ThreadRule Priority Rule 1,Finish reruling waitting queue msgs with Priority Group List [ %s ]",self._rule.getParam("priorityGroupList"))
                       self._msgForwarderQueue.put(getMsg)
                       logging.info("ThreadRule send msg to forwarder Queue with priority [%s] and  msg [%s]",getMsg[0],getMsg[1].getMessage())
                       logging.info("ThreadRule msg waittingqueue has size [ %s ] ",self._msgWaittingQueue.qsize())
                   if self._msgWaittingQueue.empty() and self._rule.getParam("ruleId")==1:
                       self._rule.setParam(ruleId=1,priorityGroupList=[])
                       logging.info("ThreadRule Priority Rule 1, Set due to empty waitting queuePriority Group List [ %s ]",self._rule.getParam("priorityGroupList"))   
                   self._queue.task_done()
               
           else :
               # groupId=-1 belongs to special kind of message : cancelation, termination or change rule message
               if json.loads(msg.getMsgBody()) is dict:
                  msgBodyKeys=json.loads(msg.getMsgBody()).keys()
                  for k in msgBodyKeys :
                      if k=="cancelation" :
                          # exmaple of msg body of two cancelation msgs : { "cancelation":[2,3]}, or { "cancelation":[3]}
                          # the first  means that group id 2,3 should be cancelled
                          # the second means that group id 2 should be processed again and only 3 should be cancelled further
                          # { "cancelation":[]} means that all group shoudl be processed further in normal way with given rule
                          if len(json.loads(msg.getMsgBody())[k])>0 :
                              self._ruleCancelation.setParam(ruleId=4,k=json.loads(msg.getMsgBody())[k])
                              logging.info("ThreadRule Rule Cancelation has been set with  msg [ %s ] and group id that should be cancelled are [ %s ]",msg.getMessage(), json.loads(msg.getMsgBody())[k])
                          else :
                              # it was recieved { "cancelation":[]} and no group id should be cancelled
                              self._ruleCancelation.setParam(ruleId=None,k=None)
                              logging.info("ThreadRule Rule Cancelation has been off set with  msg [ %s ] and all group id shoudl be processed normal way",msg.getMessage())
                      if k=="termination":
                          # termination is similiar as for cancelation groups
                          # { "termination":[2,3]}, or { "termination":[3]}, or { "termination":[]}
                          if len(json.loads(msg.getMsgBody())[k])>0 :
                              self._ruleTermination.setParam(ruleId=5,k=json.loads(msg.getMsgBody())[k])
                              logging.info("ThreadRule Rule Termination has been set with  msg [ %s ] and  group [ %s ]",msg.getMessage(),json.loads(msg.getMsgBody())[k])
                          else :
                              # it was recieved { "termination":[]} and no group should be terminated any longer
                              self._ruleTermination.setParam(ruleId=None,k=None)
                              logging.info("ThreadRule Rule Termination has been off set with  msg [ %s ] and  any group id should not be terminated any longer",msg.getMessage())
                               
                      if k=="updateRule" :
                          # example of msg body for rule update{ "updateRule":2, "priorityGroupList":[2,4]}, {"updateRule":3, "modulo":[2],"remainderList":[1] }
                          # {"updateRule":1}
                          if json.loads(msg.getMsgBody())["updateRule"]==1 :
                              self._rule.setParam(ruleId=1,priorityGroupList=[])
                              logging.info("ThreadRule rule has been updated with msg [ %s ] and ruleId [ %s ]",msg.getMsgBody(),1)
                              # rule update counter is incremented only in the positive rule update msg
                              self._ruleUpdateCounter+=1
                              logging.info("ThreadRule increment Rule counter to value [ %s ]",self._ruleUpdateCounter)
                          if json.loads(msg.getMsgBody())["updateRule"]==2 :
                              if "priorityGroupList" in msgBodyKeys :
                                  self._rule.setParam(ruleId=2, priorityGroupList=json.loads(msg.getMsgBody())["priorityGroupList"])
                                  logging.info("ThreadRule rule has been updated with msg [ %s ] and ruleId [ %s ], priority GroupList is [ %s ]",msg.getMsgBody(),2,json.loads(msg.getMsgBody())["priorityGroupList"])
                                  # rule update counter is incremented only in the positive rule update msg
                                  self._ruleUpdateCounter+=1
                                  logging.info("ThreadRule increment Rule counter to value [ %s ]",self._ruleUpdateCounter)
                              else :
                                  logging.info("ThreadRule update to rule id 2  has been malformed [ %s ]", msg.getMsgBody())
                          
                          if json.loads(msg.getMsgBody())["updateRule"]==3 :
                              if ("modulo" in msgBodyKeys)  and ("remainderList" in msgBodyKeys) :
                                  self._rule.setParam(ruleId=3, modulo=json.loads(msg.getMsgBody())["modulo"], remainderList=json.loads(msg.getMsgBody())["remainderList"])
                                  logging.info("ThreadRule rule has been updated with msg [ %s ] and ruleId [ %s ], modulo is [ %s ], remainder List is [ %s ]",msg.getMsgBody(),3,json.loads(msg.getMsgBody())["moduloi"],json.loads(msg.getMsgBody())["remainderList"])
                                  self._ruleUpdateCounter+=1
                                  logging.info("ThreadRule increment Rule counter to value [ %s ]",self._ruleUpdateCounter)
                              else :
                                  logging.info("ThreadRule update to rule id 3 has been malformed [ %s ]", msg.getMsgBody())    
                      self._queue.task_done()
