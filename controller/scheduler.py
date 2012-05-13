import threading
import time
from log import get_log
from datetime import datetime, timedelta

# cron-like scheduler 
# modified from http://stackoverflow.com/questions/373335/suggestions-for-a-cron-like-scheduler-in-python
class UniversalMatch(set):
    def __contains__(self, item):
        return True

    def __str__(self):
        return "*"

def to_set(match):
    if isinstance(match, (int, long)):
        return set([match])
    if not isinstance(match, set):
        return set(match)
    return match

universal = UniversalMatch()

class RescheduleException(Exception):
    def __init__(self, minute=universal, hour=universal,
                       day=universal, month=universal,
                       daysofweek=universal):
        self.minutes = to_set(minute)
        self.hours = to_set(hour)
        self.days = to_set(day)
        self.months = to_set(month)
        self.daysofweek = to_set(daysofweek)

class Event(object):
    WEEKDAYS = range(0,5)   # monday-friday
    WEEKEND = range(6,8)    # saturday-sunday

    def __init__(self, action, minute=universal, hour=universal, 
                       day=universal, month=universal, 
                       daysofweek=universal,
                       args=(), kwargs={}):
        self.action = action
        self.minutes = to_set(minute)
        self.hours = to_set(hour)
        self.days = to_set(day)
        self.months = to_set(month)
        self.daysofweek = to_set(daysofweek)
        self.args = args
        self.kwargs = kwargs
        self.log = get_log(self)

    def __str__(self):
        try:
            return "%s(%s)" % (self.action.__name__, id(self))
        except:
            return "Unknown(%s)" % id(self)

    def __repr__(self):
        return str(self)

    def matchtime(self, t1):
        return ((t1.minute     in self.minutes) and
                (t1.hour       in self.hours) and
                (t1.day        in self.days) and
                (t1.month      in self.months) and
                (t1.weekday()  in self.daysofweek))

    def check(self, t):
        if self.matchtime(t):
            self.log.debug("Running action '%s' args=%s kwargs=%s" % \
                    (self.action.__name__, self.args, self.kwargs))
            self.log.debug("m=%s h=%s d=%s mon=%s dow=%s" % \
                    (self.minutes, self.hours, self.days, 
                     self.months, self.daysofweek))
            self.action(*self.args, **self.kwargs)


class Scheduler:
    __shared_state = {}

    def __init__(self, *args, **kwargs):
        self.__dict__ = self.__shared_state
        self.log = get_log(self)
        if getattr(self, "initialized", None) is None:
            self.running = True
            self.cond = threading.Condition()
            self.events = []
            self.th = None
            self.initialized = True

    def register(self, *args):
        self.events.extend(args)
        self.log.debug("Events=%s" % self.events)

    def unregister(self, *args):
        for e in args:
            self.events.remove(e)

    def run(self):
        self.log.debug("Running scheduler...")
        t = datetime(*datetime.now().timetuple()[:5])
        while self.running:
            self.log.debug("Current time: %s" % datetime.now())
            for e in self.events:
                self.log.debug("Checking event %s" % e)
                try:
                    e.check(t)
                except Exception, e:
                    self.log.exception()

            t += timedelta(minutes=1)
            n = datetime.now()
            while n < t:
                s = (t - n).seconds + 1
                self.cond.acquire()
                self.log.debug("Sleeping %s seconds" % s)
                self.cond.wait(s)
                self.log.debug("Awake")
                self.cond.release()
                if not self.running:
                    break
                n = datetime.now()
        self.log.debug("Exiting scheduler...")

    def start(self):
        self.th = threading.Thread(target=self.run)
        self.th.start()

    def stop(self):
        if self.th is None:
            return
        self.cond.acquire()
        self.running = False
        self.cond.notify()
        self.cond.release()


