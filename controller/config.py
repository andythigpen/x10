import os
from ConfigParser import SafeConfigParser
from log import get_log

log = get_log("config")
filename = "%s/default.cfg" % os.path.realpath(os.path.dirname(__file__))

# A Borg config class so that all configuration objects are the same
# when configuration values change
class DefaultConfig(SafeConfigParser):
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        SafeConfigParser.__init__(self)

    def save(self):
        f = open(filename, 'w')
        try:
            self.write(f)
        except:
            log.exception()
        finally:
            f.close()

def get_config():
    config = DefaultConfig()
    config.read(filename)
    return config

