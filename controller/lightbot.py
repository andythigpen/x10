import os
import threading
from serial import Serial,SerialException
from log import get_log
import config

log = get_log("lightbot")
cfg = config.get_config()

serial = None
for i in range(0,5):
    try:
        device = '/dev/ttyUSB%s' % i
        log.debug("Trying device %s" % device)
        serial = Serial(device, timeout=2)
        log.debug("Using device %s" % device)
        break
    except SerialException:
        continue

serial_lock = threading.Lock()

AMBIENT     = True
LIVING_ROOM = cfg.get('living_room', 'house')
LIGHTS      = cfg.get('living_room', 'unit')

X10_ON     = '|'
X10_OFF    = 'O'
X10_BRIGHT = '+'
X10_DIM    = '-'

QUERY_SENSOR = 's'

lights = {}
# defaults
lights[LIVING_ROOM+LIGHTS] = 0

scenes = {}
for scene,value in cfg.items('scenes'):
    try:
        scenes[scene] = int(value)
    except:
        log.exception()


MIN_LEVEL = cfg.getint('levels', 'min')
MIN_DIM   = cfg.getint('levels', 'min_dim')
MAX_LEVEL = cfg.getint('levels', 'max')

VALID_RESPONSE = "Sent X10 command"

def x10(house, unit, repeat, action):
    '''X10 commands are prefixed with an x.'''
    x = "x%s%s%s%s" % (house, unit, repeat, action)
    log.debug("x10 %s" % x)
    return x

def lights_on(repeat=2):
    serial_lock.acquire()
    log.debug("on repeat=%s" % repeat)
    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_ON))
    result = serial.readline()
    serial_lock.release()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] = MAX_LEVEL
        return True
    return False

def lights_off(repeat=2):
    serial_lock.acquire()
    log.debug("off repeat=%s" % repeat)
    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_OFF))
    result = serial.readline()
    serial_lock.release()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] = MIN_LEVEL
        return True
    return False

def lights_dim(repeat=4):
    log.debug("dim repeat=%s" % repeat)
    if lights[LIVING_ROOM + LIGHTS] <= MIN_DIM:
        lights[LIVING_ROOM + LIGHTS] = MIN_DIM
        # return True

    serial_lock.acquire()
    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_DIM))
    result = serial.readline()
    serial_lock.release()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] -= int(repeat)
        return True
    return False

def lights_bright(repeat=4):
    log.debug("bright repeat=%s" % repeat)
    if lights[LIVING_ROOM + LIGHTS] >= MAX_LEVEL:
        lights[LIVING_ROOM + LIGHTS] = MAX_LEVEL
        # return True

    serial_lock.acquire()
    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_BRIGHT))
    result = serial.readline()
    serial_lock.release()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] += int(repeat)
        return True
    return False

def lights_scene(scene="none"):
    try:
        target = scenes[scene]
    except KeyError:
        log.exception()
        return False

    log.debug("Executing scene '%s'" % scene)
    count = 10
    val = query_sensor() 
    log.debug("Current level:%s target:%s" % (val,target))
    if val > target:
        while val > target and count > 0:
            diff = val - target
            repeat = 2
            if diff > 70:
                repeat = 8
            elif diff > 30:
                repeat = 4
            lights_dim(repeat)
            val = query_sensor()
            count -= 1
            log.debug("dim level:%s target:%s" % (val, target))

        log.debug("Current level:%s target:%s" % (val, target))
        return True

    while val < target and count > 0:
        diff = target - val
        repeat = 2
        if diff > 50:
            repeat = 8
        elif diff > 20:
            repeat = 4

        lights_bright(repeat)
        val = query_sensor()
        count -= 1
        log.debug("bright level:%s target:%s" % (val, target))

    log.debug("finish level:%s target:%s" % (val, target))
    return True

def lights_set_ambient_active(active=True):
    global AMBIENT
    if type(active) == str:
        active = active.lower() == "true"
    AMBIENT = active
    log.debug("set_ambient_active ambient=%s %s" % (AMBIENT, type(AMBIENT)))
    return True

def lights_set_ambient(enable=True):
    cfg.set('ambient', 'enabled', enable)
    cfg.save()
    return True

def lights_save_ambient_levels(low=0, high=0, maximum=0):
    cfg.set('ambient', 'low', low)
    cfg.set('ambient', 'high', high)
    cfg.set('ambient', 'max', maximum)
    cfg.save()
    return True

def status():
    status = {}
    sensor = query_sensor()
    status.update(lights)
    status['sensor'] = sensor
    status['ambient'] = AMBIENT
    return status

def query_sensor():
    log.debug("query_sensor")
    serial_lock.acquire()
    serial.write(QUERY_SENSOR)
    result = serial.readline()
    serial_lock.release()
    if not result:
        log.debug("Unable to read sensor value") 
        return False
    try:
        result = int(result.strip())
    except ValueError:
        result = False
    log.debug("Sensor value: %s" % result) 
    return result


