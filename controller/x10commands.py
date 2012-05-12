
LIVING_ROOM = 'A'
LIGHTS      = '1'

X10_ON     = '|'
X10_OFF    = 'O'
X10_BRIGHT = '+'
X10_DIM    = '-'

QUERY_SENSOR = 's'

def x10(house, unit, repeat, action):
    return "x%s%s%s%s" % (house, unit, repeat, action)

