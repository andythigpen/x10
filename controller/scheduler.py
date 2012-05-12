import threading
import time
from datetime import datetime, timedelta

# cron-like scheduler 
# modified from http://stackoverflow.com/questions/373335/suggestions-for-a-cron-like-scheduler-in-python
class UniversalMatch(set):
    def __contains__(self, item):
        return True

def to_set(match):
    if isinstance(match, (int, long)):
        return set([match])
    if not isinstance(match, set):
        return set(match)
    return match

universal = UniversalMatch()

class Event:
    def __init__(self, action, minute=universal, hour=universal, 
                       day=universal, month=universal, 
                       daysofweek=universal,
                       args=(), kwargs={}):
        self.minutes = to_set(minute)
        self.hours = to_set(hour)
        self.days = to_set(day)
        self.months = to_set(month)
        self.daysofweek = to_set(daysofweek)
        self.args = args
        self.kwargs = kwargs

    def matchtime(self, t1):
        return ((t1.minute     in self.mins) and
                (t1.hour       in self.hours) and
                (t1.day        in self.days) and
                (t1.month      in self.months) and
                (t1.weekday()  in self.daysofweek))

    def check(self, t):
        if self.matchtime(t):
            self.action(*self.args, **self.kwargs)


class Scheduler(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Scheduler, self).__init__(*args, **kwargs)
        self.running = True
        self.cond = threading.Condition()
        self.events = []

    def register(self, event):
        self.events.append(event)

    def unregister(self, event):
        self.events.remove(event)

    def run(self):
        t = datetime(*datetime.now().timetuple()[:5])
        while self.running:
            for e in self.events:
                e.check(t)

            t += timedelta(minutes=1)
            n = datetime.now()
            while n < t:
                s = (t - n).seconds + 1
                # time.sleep(s)
                self.cond.acquire()
                self.cond.wait(s)
                self.cond.release()
                if not self.running:
                    break
                n = datetime.now()

    def stop(self):
        self.cond.acquire()
        self.running = False
        self.cond.notify()
        self.cond.release()


