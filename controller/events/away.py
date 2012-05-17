import random
import lightbot
from log import get_log
from scheduler import Scheduler,Event
from config import get_config

cfg = get_config()
log = get_log('away')

def turn_off_lights():
    log.info("Turning off lights") 
    lightbot.lights_off()

def turn_on_lights():
    log.info("Turning on lights") 
    lightbot.lights_on()
    
def load():
    scheduler = Scheduler()
    # a little randomness...
    scheduler.register('away',
        Event(turn_on_lights, 
            hour=random.randint(16,19), 
            minute=random.randint(0,60),
            daysofweek=[Event.MONDAY, Event.WEDNESDAY, Event.SUNDAY]
        ),
        Event(turn_off_lights, 
            hour=random.randint(21,23), 
            minute=random.randint(0,60),
            daysofweek=[Event.MONDAY, Event.WEDNESDAY, Event.SUNDAY]
        ),

        Event(turn_on_lights, 
            hour=random.randint(16,19), 
            minute=random.randint(0,60),
            daysofweek=[Event.TUESDAY, Event.FRIDAY]
        ),
        Event(turn_off_lights, 
            hour=random.randint(21,23), 
            minute=random.randint(0,60),
            daysofweek=[Event.TUESDAY, Event.FRIDAY]
        ),

        Event(turn_on_lights, 
            hour=random.randint(17,19), 
            minute=random.randint(0,60),
            daysofweek=[Event.THURSDAY, Event.SATURDAY]
        ),
        Event(turn_off_lights, 
            hour=random.randint(22,23), 
            minute=random.randint(0,60),
            daysofweek=[Event.THURSDAY, Event.SATURDAY]
        ),
    )

load()



