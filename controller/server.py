#!/usr/bin/env python

import os
import serial
import bottle
from bottle import request, route, static_file

from scheduler import Scheduler
from log import get_log
import lightbot
import programs

# load all events...
from events import *

log = get_log("server")

@route('/ambient<action:re:(/[^/]*){0,1}>')
def index(action=''):
    if action == '/enable':
        lightbot.AMBIENT = True
    elif action == '/disable':
        lightbot.AMBIENT = False
    return '%s<b>%s</b>' % (action,lightbot.AMBIENT)

@route('/lights', method=['GET','POST'])
def lights():
    if not request.forms:        # GET
        return lightbot.status()

    # POST
    obj = request.forms
    func = getattr(lightbot, "lights_%s" % obj.get('action', ''), None)
    if func:
        if obj.get('arg', None):
            func(obj.get('arg'))
        else:
            func()
        return lightbot.status()
    return {'error': "action '%s' not found" % obj.get('action', '')}

@route('/programs', method=['GET','POST'])
def progs():
    if not request.forms:        # GET
        return programs.status()

    obj = request.forms
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
    d = os.path.realpath(os.path.dirname(__file__))
    return static_file(path, root='%s/static' % d)


def run():
    s = Scheduler()
    s.start()
    try:
        bottle.run(host='', port=6060)
    except KeyboardInterrupt:
        pass
    s.stop()

if __name__ == "__main__":
    run()

