import unittest, os, sys
from MessageGenerator import MessageGenerator
from message import Message

# @test  Test suite for class MessageGenerator
class TestMessageGenerator(unittest.TestCase):

    ## Check that the MessageGenerator class can be initialised.
    def testInit(self):
        
        msgGen=MessageGenerator(msgBurstSize=9, msgGroupIdRange=10)
        self.assertIsInstance(msgGen,MessageGenerator)
        
        msgGen=MessageGenerator(msgBurstSize=9)
        self.assertIsInstance(msgGen,MessageGenerator)

        msgGen=MessageGenerator(msgGroupIdRange=10)
        self.assertIsInstance(msgGen,MessageGenerator)
        
        with self.assertRaises(AssertionError):
           msgGen=MessageGenerator(msgGroupIdRange=2.3)
        
        with self.assertRaises(AssertionError):
           msgGen=MessageGenerator(msgGroupIdRange=-1)
        
        with self.assertRaises(AssertionError):
           msgGen=MessageGenerator(msgBurstSize=2.3)
        
        with self.assertRaises(AssertionError):
           msgGen=MessageGenerator(msgBurstSize=-1)

## @test Test suite for Generating messages from MessageGenerator
class TestMessageGeneratorGenerateMsgs(unittest.TestCase):

    ## Init test generators.
    def setUp(self):
        ## Test generator 1
        self.g1 = msgGen=MessageGenerator(msgBurstSize=5, msgGroupIdRange=5)
        ## Test generator 2
        self.g2 = msgGen=MessageGenerator(msgBurstSize=10, msgGroupIdRange=10)

    ## Delete test generators.
    def tearDown(self):
        del self.g1
        del self.g2

    ## Test that GenValue only accepts sensible inputs.
    def testGeneraetMsgs(self):

            msgList1=self.g1.generateMsgs()
            msgList2=self.g2.generateMsgs()
            
            for m in msgList1:
               self.assertLess(m.getMsgGroupId(),6)
               self.assertGreater(m.getMsgGroupId(),0)
            self.assertEqual(len(msgList1),5)
            
            for m in msgList2:
               self.assertLess(m.getMsgGroupId(),11)
               self.assertGreater(m.getMsgGroupId(),0)
            self.assertEqual(len(msgList2),10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
