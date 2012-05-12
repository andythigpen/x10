#!/usr/bin/env python

from bottle import route, run
import serial
from scheduler import Scheduler

@route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name

s = Scheduler()
s.start()

try:
    run(host='', port=6060)
except KeyboardInterrupt:
    pass

s.stop()
