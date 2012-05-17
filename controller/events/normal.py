import time
import lightbot
from log import get_log
from scheduler import Scheduler,Event
from x10commands import *
from datetime import datetime
from config import get_config

cfg = get_config()
log = get_log('normal')

previous_value = 255

def turn_off_lights(disable_ambient=True):
    log.debug("Turning off lights") 
    lightbot.lights_off()
    lightbot.AMBIENT = not disable_ambient
    
def ambient_lights():
    global previous_value
    count = 0
    if not cfg.getboolean('ambient', 'enabled'):
        log.debug("ambient not enabled...skipping.")
        return

    low_ambient_level  = cfg.getint('ambient', 'low')
    max_ambient_level  = cfg.getint('ambient', 'max')

    value = lightbot.query_sensor()
    log.debug("ambient_lights enabled=%s current=%s prev=%s" % \
            (lightbot.AMBIENT, value, previous_value))
    if lightbot.AMBIENT and \
       value <= low_ambient_level and \
       previous_value <= low_ambient_level:
        # brighten the lights, but give up after a few tries in case 
        # something has gone wrong
        while value and value < low_ambient_level and count < 20:
            log.debug("Increasing brightness.") 
            lightbot.lights_bright(repeat=2)
            count += 1
            value = lightbot.query_sensor()
            time.sleep(0.2)

        if count == 20:
            # increasing the brightness isn't doing anything for us...
            # it's likely dark now and the lights should be all on, so turn off
            # ambient lighting until the next time period
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

def load():
    scheduler = Scheduler()
    # only perform ambient lighting from 7-8am, 4-8pm
    ambient_hours = range(7,9) + range(16, 21)
    scheduler.register('normal',
        # turn off lights at 11pm sun-thurs
        Event(turn_off_lights, hour=23, minute=0, 
              daysofweek=[Event.SUNDAY, Event.MONDAY, Event.TUESDAY, 
                          Event.WEDNESDAY, Event.THURSDAY]),
        # turn off lights at 1am on sat-sun
        Event(turn_off_lights, hour=1, minute=0, daysofweek=Event.WEEKEND),
        # turn off lights at 8:30am in case of ambient lighting on weekdays
        Event(turn_off_lights, hour=8, minute=30, daysofweek=Event.WEEKDAYS),
        Event(ambient_lights, hour=ambient_hours),
        Event(reenable_ambient_lights, hour=[7,16]),
    )

load()



