__author__ = 'mashenjun'
import ConfigParser
import logging
import os
CONFIG_FILE = "aws.config"
DEFAULT_SECTION = 'default'

class Config:

    config = None

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(open(self.get_home_dir() + CONFIG_FILE))
        self.config.read([self.get_home_dir() + CONFIG_FILE])

    def ConfigSectionMap(self):
        dict1 = {}
        section = DEFAULT_SECTION
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    logging.debug("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def get_home_dir(self):
        dir = os.getcwd()
        if not dir:
            dir = '.'
        if not dir.endswith('/'):
            dir += '/'
        return dir