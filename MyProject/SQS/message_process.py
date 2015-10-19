__author__ = 'mashenjun'

def message_process(message):
    return message.split("/")

def message_getusername(message):
    path = message.split("@")[0]
    return  path.split("/")[0]

def message_gerid(message):
    return message.split("@")[1]