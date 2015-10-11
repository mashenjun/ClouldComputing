__author__ = 'mashenjun'
import time
import boto
import boto.ec2
import logging
from configFile.instanceConfig import Config

# storage service
# s3 = boto.connect_s3()
# should make a file to save configuration
config = Config()

def launch_default_instance():
    logger = logging.getLogger(__name__)
    conn = boto.ec2.connect_to_region(config.ConfigSectionMap()["region"])
    reservations = conn.start_instances("i-804dfb41")
    instance = reservations.instances[0]
    while instance.state != "running":
        time.sleep(5)
        instance.update()
    logger.info('Instance %s with DNS %s started' % (instance.id, instance.public_dns_name))
    instance.monitor() #enable the monitor

def launch_instance():
    logger = logging.getLogger(__name__)
    conn = boto.ec2.connect_to_region(config.ConfigSectionMap()["region"])
    reservations = conn.start_instances("i-804dfb41")
    instance = reservations.instances[0]
    while instance.state != "running":
        time.sleep(5)
        instance.update()
    logger.info('Instance %s with DNS %s started' % (instance.id, instance.public_dns_name))
    instance.monitor() #enable the monitor