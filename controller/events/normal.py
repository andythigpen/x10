import serial
import time
from log import get_log
from scheduler import Scheduler,Event
from x10commands import *
from datetime import datetime

enabled = True
device = '/dev/ttyUSB1'
# Arduino will return a result from 0-255, from experimentation 170 seems about 
# the right level to start brightening the lights
enable_ambient     = True
low_ambient_level  = 170
high_ambient_level = 190
max_ambient_level  = 235
previous_value     = 255
# only perform ambient lighting from 7-8am, 4-8pm
ambient_hours = range(7,9) + range(16, 21)
serial = serial.Serial(device, timeout=1)

log = get_log('normal')

def turn_off_lights():
    log.debug("Turning off lights") 
    serial.write(x10(LIVING_ROOM, LIGHTS, 2, X10_OFF))
    return serial.readline()
    
def query_sensor():
    serial.write(QUERY_SENSOR)
    result = serial.readline()
    if not result:
        log.debug("Unable to read sensor value") 
        return False
    try:
        result = int(result.strip())
    except ValueError:
        result = False
    log.debug("Sensor value: %s" % result) 
    return result

def ambient_lights():
    global enable_ambient, previous_value
    count = 0
    # brighten the lights, but give up after a few tries in case 
    # something has gone wrong
    value = query_sensor()
    if enable_ambient and \
       value <= low_ambient_level and \
       previous_value <= low_ambient_level:
        while value and value < high_ambient_level and count < 10:
            log.debug("Increasing brightness.") 
            serial.write(x10(LIVING_ROOM, LIGHTS, 4, X10_BRIGHT))
            serial.readline()
            count += 1
            value = query_sensor()
            time.sleep(0.2)
        # we detected an an ambient light event for this time period...
        # don't increase brightness again until next time period
        # leave it scheduled so that if max_ambient_level is reached during 
        # this time, the lights will turn off
        enable_ambient = False

    if value and value >= max_ambient_level and \
       previous_value >= max_ambient_level:
        log.debug("Sensor greater than max_ambient_level. Turning off lights.") 
        serial.write(x10(LIVING_ROOM, LIGHTS, 2, X10_OFF))

    previous_value = value

# re-enables the ambient lights for the next time
def reenable_ambient_lights():
    enable_ambient = True

if enabled:
    s = Scheduler()
    s.register(
        Event(turn_off_lights, minute=0, hour=23, daysofweek=Event.WEEKDAYS),
        Event(turn_off_lights, minute=0, hour=1, daysofweek=Event.WEEKEND),
        # turn off lights at 8:30am in case of ambient lighting on weekdays
        Event(turn_off_lights, minute=30, hour=8, daysofweek=Event.WEEKDAYS),
        Event(ambient_lights, hour=ambient_hours),
        Event(reenable_ambient_lights, hour=[9,21]),
    )
