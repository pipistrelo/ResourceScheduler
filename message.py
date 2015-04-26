class Message:
    """Message class to handle message object""" 
    
    ## @param msgGroupId is group id in which message belongs
    ## @param msgBody is body of message
    ## @param msgsState is the state of message <created|wait|completed> created is used when message is created, wait when message is being processed, completed when message 
    ## has already been processed
    def __init__(self,msgRef=None,msgGroupId=None,msgBody=None,msgState="created"):
        # special messages has group id -1 e.g. cancelation, termination, updateRule
        assert msgGroupId > -2 , "ERROR: msgGroupId has to be gretaer than -2 : -1 for special messages otherwise for other group of messages should be an  integer"
        assert isinstance(msgRef,str) , "ERROR: msgRef has to be string"
        assert isinstance(msgBody,str) , "ERROR: msgBody has to be string"
        assert isinstance(msgState,str) , "ERROR: msgState has to be sring" 
        self._msgGroupId=msgGroupId
        self._msgBody=msgBody
        self._msgState=msgState
        self._msgRef=msgRef
        self._message={}
        if (self._msgRef and self._msgGroupId and self._msgBody and self._msgState) :
            self._message["ref"]=self._msgRef
            self._message["groupId"]=self._msgGroupId
            self._message["body"]=self._msgBody
            self._message["state"]=self._msgState
        else : 
            self._message=None
             
    def getMessage(self):
        return self._message
    
    def getMsgRef(self):
        if self._message :
            return self._message["ref"]
        else :
            return None

    def getMsgGroupId(self):
        if self._message :
            return self._message["groupId"]
        else : 
            return None
   
    def getMsgBody(self):
        if self._message :
            return self._message["body"]
        else : 
            return None

    def getMsgState(self):
        if self._message :
            return self._message["state"]
        else : 
            return None
    

    def updateMsgState(self,state):
        if state== "created" or state=="sent" or state=="completed":
           self._message["state"]=state
        else: 
           print "Wrong state provided It should be <created | sent | completed> "

    def completed(self):
        self._message["state"]="completed"   

