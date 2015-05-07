# ResourceScheduler

ResourceScheduler is a simple, configurable message broker written in Python. It is quasi producer/consumer example. Producer is simulated via MessageGenerator thread using Queues. Message scheduling is based on predefined rules that are defined within Rule class and Rule thread class (in message broker terminology, it is Exchange with their routing algorithms) . After message is properly evaluated by rule, it will be sent to Forwarder Queue (Priority Queue) if any resource is available at that time. If none resource is available, message within its assigned priority is sent to waitting queue. Any time resource becomes availabe the respective thread sends resource limited number of messages to Forwarder Queue. Forwarder Queue send message to Gateway Interface that sends message directly to Resource Queue, that populate resources. Resource is simulated via Resource thread class. After message is processed Message interface call method completed() and the respective resource is released. 
In order to test or simulate this application, Message Class is created. 
Where message has the following structure for example:

::

        {'body': '30818QoGBB', 'state': 'created', 'ref': '30818QoGBB', 'groupId': 7}

config.py file provides simple configuration of Resource Scheduler application. 
Here is a quick overview of configurable variables:

maxStep         : defines maximum number of message generation steps

maxBurstSize    : defines maximum number of messages generated in one step

msgGroupIdRange : defines maximum number of used group ids

timeSleepMaxGenerator : represents max time value for generated time variates representing  a time between two burst size group of messages send to Rule Queue

timeSleepMaxResource : represents max time value for generated time variates representing resource processing time

numberResources : represents total number of available resources


Rule definitions (It is kind of Exchanges and routing keys):

ruleId : represents the id for the respective rule

If ruleId is set to value 1, messages are handled with the following rule:
Suppose  single resource, messages received:
message1 (group2)
message2 (group1)
message3 (group2)
message4 (group3)

Processing :
message1 (group2) was received first so will be processed first as messages complete, the order they are sent to the gateway should be:
message1
message3 (it's part of group2, which is already "in-progress")
message2
message4

So preference is put on messages from group id that comes first to gateway, if none messages from that group are present in a queue, any other message comes to gateway as first changes the prefered message group id to its group id.

If ruleId is set to value 2, messages are handled with the following rule:
Messages from given groups have higher priority than messages of other groups.
Priority group list is defined in the config file:

priorityGroupList : represents list of preferred group ids e.g. [2,4,6,8,10]

if ruleId is set to value 3, messages are prioritise according to the following rule:
It takes group id of the respective message and carry out modulo operation, and the outcome is compared with the prefered remainder list. So for example if one wants to prefer odd group ids, it may set the config as :
modulo=[2]
remainderList=[1]

There is other two rule id:

ruleId = 4 : represents ruled id for cancelation messages, that needs to be separtly sent via CLI Send Message Queue, message has predefined  special "groupId"=-1, and "msgBody":'{"cancelation":[2,5]}' what means that messages from groups 2 and 5 will be cancel.

ruleId=5 : represents ruled id for termination messages, similiar as cancelation, only in msgBody the key word is changed to "termination", also the list is used to defined groups for which messages will be teraminated


In order to run application, use this command:

python main.py





