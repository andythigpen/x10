import serial
import time
from scheduler import Scheduler,Event
from x10commands import *
from datetime import datetime

enabled = True
device = '/dev/ttyUSB1'
# Arduino will return a result from 0-255, from experimentation 170 seems about 
# the right level to start brightening the lights
ambient_level = 170
max_ambient_level = 220
# only perform ambient lighting from 7-8am, 4-8pm
ambient_hours = range(7,9) + range(16, 21)
serial = serial.Serial(device, timeout=1)

def turn_off_lights():
    serial.write(x10(LIVING_ROOM, LIGHTS, 2, X10_OFF))
    return serial.readline()
    
def query_sensor():
    serial.write(QUERY_SENSOR)
    result = serial.readline()
    if not result:
        return False
    return int(result.strip())

def ambient_lights():
    count = 0
    # brighten the lights, but give up after a few tries in case 
    # something has gone wrong
    value = query_sensor()
    while value and value <= ambient_level and count < 20:
        serial.write(x10(LIVING_ROOM, LIGHTS, 2, X10_BRIGHT))
        serial.readline()
        count += 1
        value = query_sensor()
        time.sleep(1)

    if value and value >= max_ambient_level:
        serial.write(x10(LIVING_ROOM, LIGHTS, 2, X10_OFF))

if enabled:
    s = Scheduler()
    s.register(
        Event(turn_off_lights, minute=0, hour=23, daysofweek=Event.WEEKDAYS),
        Event(turn_off_lights, minute=0, hour=1, daysofweek=Event.WEEKENDS),
        # turn off lights at 8:30am in case of ambient lighting on weekdays
        Event(turn_off_lights, minute=30, hour=8, daysofweek=Event.WEEKDAYS),
        Event(ambient_lights, hour=ambient_hours)
    )
