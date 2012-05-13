#!/usr/bin/env python

from bottle import route, run, static_file
import serial
from scheduler import Scheduler
from log import get_log
import lightbot

# load all events...
from events import *

@route('/ambient<action:re:(/[^/]*){0,1}>')
def index(action=''):
    if action == '/enable':
        lightbot.AMBIENT = True
    elif action == '/disable':
        lightbot.AMBIENT = False
    return '%s<b>%s</b>' % (action,lightbot.AMBIENT)

@route('/lights<action:re:(/[^/]*){0,1}>')
def lights(action="none"):
    action = action[1:]
    if action == "":
        action = "status"
    func = getattr(lightbot, "lights_%s" % action, None)
    if func:
        func()
        return lightbot.lights_status()
    return "action '%s' not found" % action

@route('/static/<path:path>')
def static(path):
    return static_file(path, root='./static')

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
