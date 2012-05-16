import time
import lightbot
from log import get_log
from scheduler import Scheduler,Event
from x10commands import *
from datetime import datetime
from config import get_config

enabled = True
cfg = get_config()

previous_value     = 255

log = get_log('normal')

def turn_off_lights():
    log.debug("Turning off lights") 
    lightbot.lights_off()
    
def ambient_lights():
    global previous_value
    count = 0
    if not cfg.getboolean('ambient', 'enabled'):
        log.debug("ambient not enabled...skipping.")
        return

    low_ambient_level  = cfg.getint('ambient', 'low')
    high_ambient_level = cfg.getint('ambient', 'high')
    max_ambient_level  = cfg.getint('ambient', 'max')

    value = lightbot.query_sensor()
    log.debug("ambient_lights enabled=%s current=%s prev=%s" % \
            (lightbot.AMBIENT, value, previous_value))
    if lightbot.AMBIENT and \
       value <= low_ambient_level and \
       previous_value <= low_ambient_level:
        # brighten the lights, but give up after a few tries in case 
        # something has gone wrong
        while value and value < high_ambient_level and count < 10:
            log.debug("Increasing brightness.") 
            lightbot.lights_bright()
            count += 1
            value = lightbot.query_sensor()
            time.sleep(0.2)
        # we detected an an ambient light event for this time period...
        # don't increase brightness again until next time period
        # leave it scheduled so that if max_ambient_level is reached during 
        # this time, the lights will turn off
        lightbot.AMBIENT = False

    if value and value >= max_ambient_level and \
       previous_value >= max_ambient_level:
        log.debug("Sensor greater than max_ambient_level. Turning off lights.") 
        lightbot.lights_off()

    if value:
        previous_value = value

# re-enables the ambient lights for the next time
def reenable_ambient_lights():
    lightbot.AMBIENT = True

if enabled:
    s = Scheduler()
    # only perform ambient lighting from 7-8am, 4-8pm
    ambient_hours = range(7,9) + range(16, 21)
    s.register(
        Event(turn_off_lights, minute=0, hour=23, daysofweek=Event.WEEKDAYS),
        Event(turn_off_lights, minute=0, hour=1, daysofweek=Event.WEEKEND),
        # turn off lights at 8:30am in case of ambient lighting on weekdays
        Event(turn_off_lights, minute=30, hour=8, daysofweek=Event.WEEKDAYS),
        Event(ambient_lights, hour=ambient_hours),
        Event(reenable_ambient_lights, hour=[7,16]),
    )

#TODO use load/unload functions so that different schedulers can be 
# loaded/unloaded during runtime

