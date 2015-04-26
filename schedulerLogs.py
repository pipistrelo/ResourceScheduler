import logging

FORMAT = "%(asctime)-15s %(levelname)s: %(threadName)s  %(thread)d  %(message)s"
DATEFORMAT='%m/%d/%Y %I:%M:%S %p'
logging.basicConfig(filename="logScheduler.log", filemode='w', format=FORMAT,datefmt=DATEFORMAT,level=logging.DEBUG)
