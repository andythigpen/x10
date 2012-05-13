#!/usr/bin/env python

import sys
from daemon import Daemon
from scheduler import Scheduler
from log import get_log
from bottle import run

class Controller(Daemon):
    def run(self):
        log = get_log("daemon")
        import server
        try:
            server.run()
        except:
            log.exception()

if __name__ == "__main__":
    daemon = Controller('/tmp/controller.pid')
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            daemon.start()
        elif sys.argv[1] == 'stop':
            daemon.stop()
        elif sys.argv[1] == 'restart':
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
