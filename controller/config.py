import os
from ConfigParser import ConfigParser

def get_config():
    cfgfilename = "%s/default.cfg" % os.path.realpath(
            os.path.dirname(__file__))
    config = ConfigParser()
    config.read(cfgfilename)
    return config

