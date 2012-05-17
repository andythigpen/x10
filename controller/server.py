#!/usr/bin/env python

import os
import inspect
import serial
import bottle
from bottle import request, route, static_file, template

from scheduler import Scheduler
from log import get_log
from config import get_config
import lightbot
import programs

# load all events...
from events import *

log = get_log("server")

@route('/')
def index(action=''):
    return template('main')

@route('/lights', method=['GET','POST'])
def lights():
    if not request.forms:        # GET
        return lightbot.status()

    # POST
    obj = request.forms
    func = getattr(lightbot, "lights_%s" % obj.get('action', ''), None)
    if not func:
        log.debug("action '%s' not found" % obj.get('action', ''))
        return {'error': "action '%s' not found" % obj.get('action', '')}

    # only keyword arguments allowed
    kwargs = {}
    spec = inspect.getargspec(func)
    for variable in spec.args:
        value = obj.get(variable, None)
        if not value is None:
            kwargs[variable] = value

    func(**kwargs)
    return lightbot.status()

@route('/programs', method=['GET','POST'])
def progs():
    if not request.forms:        # GET
        return programs.status()

    obj = request.forms
    func = getattr(programs, "%s_%s" % (obj.get('action', ''), 
        obj.get('program', '')), None)
    if not func:
        log.debug("action '%s' not found" % obj.get('action', ''))
        return {'error': "action '%s' not found" % obj.get('action','')}

    # only keyword arguments allowed
    kwargs = {}
    spec = inspect.getargspec(func)
    for variable in spec.args:
        value = obj.get(variable, None)
        if not value is None:
            kwargs[variable] = value

    func(**kwargs)
    return programs.status()

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

@route('/scheduler', method=['POST'])
def schedule():
    obj = request.forms
    if not obj or obj.get('name', None) is None:
        return {'msg': 'Missing form or variable name.'}

    name = obj.get('name')
    cfg = get_config()
    cfg.set('scheduler', 'active', name)
    cfg.save()
    return {'msg': "Active schedule is now '%s'" % name}

def run():
    s = Scheduler()
    s.start()
    try:
        templates = "%s/views" % os.path.realpath(os.path.dirname(__file__))
        bottle.TEMPLATE_PATH.insert(0, templates)
        # bottle.debug(True)
        bottle.run(host='', port=6060) #, reloader=True)
    except KeyboardInterrupt:
        pass
    s.stop()

if __name__ == "__main__":
    run()

