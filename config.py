# configure function fillMsgGeneratorQueue that generate queue with tuples (maxBurstSize, msgGroupIdRange) with ranodm values 
# for given step
# step is one burst of messages
maxStep=20
maxBurstSize=30
msgGroupIdRange=10

# Time sleep time for Messagegenerator thread 
# timeSleepMax represents max time value for generate time variates representing  a time between two burst size group of messages send to Rule Queue
timeSleepMaxGenerator=1

# numer of resorces
numberResources=5

# timeSleepMax represents max time value for generate time variates representing resource processing time
timeSleepMaxResource=1

#Basic Rules
# rule Id for Rule class
ruleId=3

# if ruleId=2
priorityGroupList=[2,4,6,8,10]

#if ruleId=3
modulo=[2]
remainderList=[1]
