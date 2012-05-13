from serial import Serial,SerialException
from log import get_log

log = get_log('lightbot')

serial = None
for i in range(0,5):
    try:
        device = '/dev/ttyUSB%s' % i
        log.debug("Trying device %s" % device)
        serial = Serial(device, timeout=1)
        log.debug("Using device %s" % device)
        break
    except SerialException:
        continue


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

MIN_LEVEL = 0
MIN_DIM   = 4
MAX_LEVEL = 24

VALID_RESPONSE = "Sent X10 command"

def x10(house, unit, repeat, action):
    '''X10 commands are prefixed with an x.'''
    return "x%s%s%s%s" % (house, unit, repeat, action)

def lights_on(repeat=2):
    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_ON))
    result = serial.readline()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] = MAX_LEVEL
        return True
    return False

def lights_off(repeat=2):
    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_OFF))
    result = serial.readline()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] = MIN_LEVEL
        return True
    return False

def lights_dim(repeat=4):
    if lights[LIVING_ROOM + LIGHTS] <= MIN_DIM:
        lights[LIVING_ROOM + LIGHTS] = MIN_DIM
        return True

    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_DIM))
    result = serial.readline()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] -= repeat
        return True
    return False

def lights_bright(repeat=4):
    if lights[LIVING_ROOM + LIGHTS] >= MAX_LEVEL:
        lights[LIVING_ROOM + LIGHTS] = MAX_LEVEL
        return True

    serial.write(x10(LIVING_ROOM, LIGHTS, repeat, X10_BRIGHT))
    result = serial.readline()
    log.debug("Serial response: %s" % result)
    if VALID_RESPONSE in result:
        lights[LIVING_ROOM + LIGHTS] += repeat
        return True
    return False

def status():
    status = {}
    sensor = query_sensor()
    status.update(lights)
    status['sensor'] = sensor
    status['ambient'] = AMBIENT
    return status

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


