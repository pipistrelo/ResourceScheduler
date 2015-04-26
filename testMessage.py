import unittest, os, sys
from message import Message

# @test  Test suite for class Message
class TestRule(unittest.TestCase):

    ## Check that the Rule class can be initialised.
    def testInit(self):
        
        msg=Message(msgRef="1a",msgGroupId=3,msgBody="2a")
        self.assertIsInstance(msg, Message)

        with self.assertRaises(AssertionError):
           Message(msgRef=1,msgGroupId=3,msgBody="2a")
 
        with self.assertRaises(AssertionError):
           Message(msgRef="11a",msgGroupId=-2,msgBody="2a")

        with self.assertRaises(AssertionError):
           Message(msgRef="1a",msgGroupId=3,msgBody=3)





## @test Test suite for Message get,updateMsg and completed 
class TestMessageMethods(unittest.TestCase):

    ## Init test generators.
    def setUp(self):
        ## Test generator 1
        self.g1 = msg=Message(msgRef="1a",msgGroupId=1,msgBody="2a")
        ## Test generator 2
        self.g2 = msg=Message(msgRef="3a",msgGroupId=2,msgBody="4a")

    ## Delete test generators.
    def tearDown(self):
        del self.g1
        del self.g2

    ## Test that get methods
    def testGetMethods(self): 
    
        self.assertEqual(self.g1.getMessage(),{'body': '2a', 'state': 'created', 'ref': '1a', 'groupId': 1})
        self.assertEqual(self.g2.getMessage(),{'body': '4a', 'state': 'created', 'ref': '3a', 'groupId': 2})

        self.assertEqual(self.g1.getMsgRef(),'1a')
        self.assertEqual(self.g2.getMsgRef(),'3a')

        self.assertEqual(self.g1.getMsgGroupId(),1)
        self.assertEqual(self.g2.getMsgGroupId(),2)

        self.assertEqual(self.g1.getMsgBody(),'2a')
        self.assertEqual(self.g2.getMsgBody(),'4a')

        self.assertEqual(self.g1.getMsgState(),'created')
        self.assertEqual(self.g2.getMsgState(),'created')

    ## Test that updateMsg methods
    def testUpdateMsg(self):      
    
        self.g1.updateMsgState("sent")
        self.g2.updateMsgState("sent")
        self.assertEqual(self.g1.getMsgState(),'sent')
        self.assertEqual(self.g2.getMsgState(),'sent')

        self.g1.updateMsgState("completed")
        self.g2.updateMsgState("completed")
        self.assertEqual(self.g1.getMsgState(),'completed')
        self.assertEqual(self.g2.getMsgState(),'completed')

        self.g1.updateMsgState("created")
        self.g2.updateMsgState("created")
        self.assertEqual(self.g1.getMsgState(),'created')
        self.assertEqual(self.g2.getMsgState(),'created')


    ## Test that completed  method
    def testUpdateMsg(self): 
    
        self.g1.completed()
        self.g2.completed()
        self.assertEqual(self.g1.getMsgState(),'completed')
        self.assertEqual(self.g2.getMsgState(),'completed')


if __name__ == "__main__":
    unittest.main(verbosity=2)
    unittest.main()
