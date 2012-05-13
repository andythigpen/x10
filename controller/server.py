#!/usr/bin/env python

from bottle import route, run
import serial
from scheduler import Scheduler
from log import get_log
import lightbot

from events import normal

# load all events...
from events import *

@route('/ambient/:enable')
def index(enable=''):
    if enable == 'enable':
        normal.enable_ambient = True
    elif enable == 'disable':
        normal.enable_ambient = False
    return '<b>%s</b>' % normal.enable_ambient

@route('/lights/<action>')
def lights(action="none"):
    func = getattr(lightbot, "lights_%s" % action, None)
    if func:
        func()
        return lightbot.lights_status()
    return "action '%s' not found" % action

if __name__ == "__main__":
    s = Scheduler()
    log = get_log("main")
    log.debug("s=%s id=%s" % (s,id(s)))
    s.start()
    try:
        run(host='', port=6060)
    except KeyboardInterrupt:
        pass
    s.stop()
