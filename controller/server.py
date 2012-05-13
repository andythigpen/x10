#!/usr/bin/env python

import serial
from bottle import request, route, run, static_file
from scheduler import Scheduler
from log import get_log
import lightbot
import programs

# load all events...
from events import *

@route('/ambient<action:re:(/[^/]*){0,1}>')
def index(action=''):
    if action == '/enable':
        lightbot.AMBIENT = True
    elif action == '/disable':
        lightbot.AMBIENT = False
    return '%s<b>%s</b>' % (action,lightbot.AMBIENT)

@route('/lights', method=['GET','POST'])
def lights():
    if not request.json:        # GET
        return lightbot.status()

    # POST
    obj = request.json
    func = getattr(lightbot, "lights_%s" % obj.get('action', ''), None)
    if func:
        func(repeat=obj.get('repeat', 2))
        return lightbot.status()
    return {'error': "action '%s' not found" % obj.get('action', '')}

@route('/programs', method=['GET','POST'])
def progs():
    if not request.json:        # GET
        return programs.status()

    obj = request.json
    func = getattr(programs, "%s_%s" % (obj.get('action', ''), 
        obj.get('program', '')), None)
    if func:
        func()
        return programs.status()
    return {'error': "action '%s' not found" % obj.get('action','')}

@route('/status')
def status():
    status = {}
    status['lights'] = lightbot.status()
    status['programs'] = programs.status()
    return status

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
