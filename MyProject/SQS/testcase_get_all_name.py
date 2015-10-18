__author__ = 'mashenjun'
import handler as sqsh

sqs,client = sqsh.connect_sqs()

list = sqsh.get_all_queue_name(sqs)
print list