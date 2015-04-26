# ResourceScheduler

ResourceScheduler is a simple, configurable message broker written in Python. It is quasi producer/consumer example. Producer is simulated via MessageGenerator using Queues. Message scheduling is based on predefined rules that are defined within Rule class. After message is properly evaluated by rule, it will be sent to Forwarder Queue (Priority Queue) if any resource is available at that time. If none resource is available, message within its assigned priority is sent to waitting queue. Any time resource becomes availabe the respective therad sends messages to Forwarder Queue. Forwarder Queue send message to Gateway Interface that sends message directly to Resource Queue, that populate resources. Resource is simulated via Resource thread class. After message is processed Message interface call method completed() and the respective resource is released.

File config.py provides simple configuration of Resource Scheduler application. 

maxStep defines =20
maxBurstSize=30
msgGroupIdRange=10
