import unittest, os, sys
from Rules import ThreadRule, msgRuleQueue, Rule
from message import Message

# @test  Test suite for class Rule
class TestRule(unittest.TestCase):

    ## Check that the Rule class can be initialised.
    def testInit(self):
        rule=Rule()
        self.assertIsInstance(rule, Rule)

        rule1=Rule(ruleId=1,priorityGroupList=[])
        self.assertIsInstance(rule1, Rule)

        rule2=Rule(ruleId=2, priorityGroupList=[2,3])
        self.assertIsInstance(rule2, Rule)

        rule3=Rule(ruleId=3, modulo=[2], remainderList=[1])
        self.assertIsInstance(rule3, Rule)

        rule4=Rule(ruleId=4,cancelation=[2,3])
        self.assertIsInstance(rule4, Rule)

        rule5=Rule(ruleId=5,termination=[3,4])
        self.assertIsInstance(rule5, Rule)

        with self.assertRaises(AssertionError):
           Rule(ruleId=1.2)
        with self.assertRaises(AssertionError):
           Rule(ruleId=[1,2,3])
        with self.assertRaises(AssertionError):
           Rule(ruleId=1,priorityGroupList=2)
        with self.assertRaises(AssertionError):
           Rule(ruleId=2,priorityGroupList=[1,1.3])
        with self.assertRaises(AssertionError):
           Rule(ruleId=3,modulo=[2,3],remainderList=[1])
        with self.assertRaises(AssertionError):
           Rule(ruleId=3,modulo=[4],remainderList=[1.3,3])

   
    ## Check run mehod
    def testRun(self):
        
        msg1=Message(msgRef="1234abcd",msgGroupId=1,msgBody="1234abcd")
        msg2=Message(msgRef="1235abcd",msgGroupId=2,msgBody="1234abcd")
        msg3=Message(msgRef="1236abcd",msgGroupId=3,msgBody="1234abcd")
        msg4=Message(msgRef="1237abcd",msgGroupId=4,msgBody="1234abcd")

        rule1=Rule(ruleId=1,priorityListGroup=[])
        rule1.setParam(priorityGroupList=[2])
        ruleMsg1Priority=rule1.run(msg1)
        ruleMsg2Priority=rule1.run(msg2)
        ruleMsg3Priority=rule1.run(msg3)
        ruleMsg4Priority=rule1.run(msg4)
        self.assertEqual(ruleMsg1Priority,2)
        self.assertEqual(ruleMsg2Priority,1)
        self.assertEqual(ruleMsg3Priority,2)
        self.assertEqual(ruleMsg4Priority,2)

        rule2=Rule(ruleId=2,priorityListGroup=[3])
        rule2.setParam(priorityGroupList=[2,4])
        ruleMsg1Priority=rule2.run(msg1)
        ruleMsg2Priority=rule2.run(msg2)
        ruleMsg3Priority=rule2.run(msg3)
        ruleMsg4Priority=rule2.run(msg4)
        self.assertEqual(ruleMsg1Priority,2)
        self.assertEqual(ruleMsg2Priority,1)
        self.assertEqual(ruleMsg3Priority,2)
        self.assertEqual(ruleMsg4Priority,1)

        rule3=Rule(ruleId=3,modulo=[2],remainderList=[1])
        rule3.setParam(remainderList=[0])
        ruleMsg1Priority=rule3.run(msg1)
        ruleMsg2Priority=rule3.run(msg2)
        ruleMsg3Priority=rule3.run(msg3)
        ruleMsg4Priority=rule3.run(msg4)
        self.assertEqual(ruleMsg1Priority,2)
        self.assertEqual(ruleMsg2Priority,1)
        self.assertEqual(ruleMsg3Priority,2)
        self.assertEqual(ruleMsg4Priority,1)

        rule4=Rule(ruleId=4,cancelation=[2])
        rule4.setParam(cancelation=[2,3])
        ruleMsg1Priority=rule4.run(msg1)
        ruleMsg2Priority=rule4.run(msg2)
        ruleMsg3Priority=rule4.run(msg3)
        ruleMsg4Priority=rule4.run(msg4)
        self.assertEqual(ruleMsg1Priority,1)
        self.assertEqual(ruleMsg2Priority,4)
        self.assertEqual(ruleMsg3Priority,4)
        self.assertEqual(ruleMsg4Priority,1)

        rule5=Rule(ruleId=5,termination=[1])
        rule5.setParam(termination=[3,1])
        ruleMsg1Priority=rule5.run(msg1)
        ruleMsg2Priority=rule5.run(msg2)
        ruleMsg3Priority=rule5.run(msg3)
        ruleMsg4Priority=rule5.run(msg4)
        self.assertEqual(ruleMsg1Priority,5)
        self.assertEqual(ruleMsg2Priority,1)
        self.assertEqual(ruleMsg3Priority,5)
        self.assertEqual(ruleMsg4Priority,1)


    ## Check that the setParam and getParam ethod
    def testSetParamGetParam(self):
        
        rule1=Rule(ruleId=1)
        self.assertEqual(rule1.getParam("ruleId"),1)
        rule1.setParam(priorityGroupList=[2,4])
        self.assertEqual(rule1.getParam("priorityGroupList"),[2,4]) 
        rule1.setParam(ruleId=3,modulo=[4],remainderList=[0,1])
        self.assertEqual(rule1.getParam("modulo"),[4])
        self.assertEqual(rule1.getParam("remainderList"),[0,1])
        rule1.setParam(ruleId=4,cancelation=[4,7])
        self.assertEqual(rule1.getParam("cancelation"),[4,7])
        rule1.setParam(ruleId=5,termination=[5,9])
        self.assertEqual(rule1.getParam("termination"),[5,9])




if __name__ == "__main__":
    unittest.main(verbosity=2)
    unittest.main()
