import threading
from serial import Serial,SerialException
from log import get_log

log = get_log('lightbot')

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
LIVING_ROOM = 'A'
LIGHTS      = '1'

X10_ON     = '|'
X10_OFF    = 'O'
X10_BRIGHT = '+'
X10_DIM    = '-'

QUERY_SENSOR = 's'

lights = {}
# defaults
lights[LIVING_ROOM+LIGHTS] = 0

scenes = {
    "low"    : 100,
    "medium" : 140,
    "high"   : 190,
}

MIN_LEVEL = 0
MIN_DIM   = 4
MAX_LEVEL = 24

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
        lights[LIVING_ROOM + LIGHTS] -= repeat
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
        lights[LIVING_ROOM + LIGHTS] += repeat
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

def lights_set_ambient(enable=True):
    global AMBIENT
    if type(enable) == str:
        enable = str(enable).lower() == "true"
    AMBIENT = enable
    log.debug("set_ambient ambient=%s %s" % (AMBIENT, type(AMBIENT)))
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


