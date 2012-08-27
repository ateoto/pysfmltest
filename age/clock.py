import sfml as sf
import sys
import time

class ScheduledItem(object):
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

class ScheduledIntervalItem(object):
    def __init__(self, func, interval, last_ts, next_ts, args, kwargs):
        self.func = func
        self.interval = interval
        self.last_ts = last_ts
        self.next_ts = next_ts
        self.args = args
        self.kwargs = kwargs

class GameClock(sf.Clock):

    def __init__(self):
        super(GameClock, self).__init__()
        if sys.platform in ('win32', 'cygwin'):
            self.time = time.clock
        else:
            self.time = time.time

        self.started = self.time()
        self.last_ts = self.started
        
        self.scheduled_items = list()
        self.scheduled_interval_items = list()

    def update(self):
        ts = self.time()
        dt = ts - self.last_ts
        
        to_remove = list()

        for item in self.scheduled_items:
            item.func(dt, *item.args, **item.kwargs)

        for item in self.scheduled_interval_items:
            if ts >= item.next_ts:
                item.func(dt, *item.args, **item.kwargs)
                if item.interval > 0:
                    item.last_ts = ts
                    item.next_ts = ts + item.interval
                else:
                    to_remove.append(item)

        for item in to_remove:
            self.scheduled_interval_items.remove(item)
        
        self.restart()
        self.last_ts = ts


    def sort_scheduled_interval_items(self):
        self.scheduled_interval_items.sort(key=lambda a: a.next_ts)

    def schedule(self, func, *args, **kwargs):
        self.scheduled_items.append(ScheduledItem(func, args, kwargs))

    def _schedule_item(self, func, last_ts, next_ts, interval, *args, **kwargs):
        self.scheduled_interval_items.append(
                ScheduledIntervalItem(func, interval, last_ts, next_ts, args, kwargs))


    def schedule_interval(self, func, interval, *args, **kwargs):
        last_ts = self.last_ts
        next_ts = last_ts + interval
        self._schedule_item(func, last_ts, next_ts, interval, *args, **kwargs)
        self.sort_scheduled_interval_items()

    def schedule_once(self, func, delay, *args, **kwargs):
        last_ts = self.last_ts
        next_ts = last_ts + delay
        self._schedule_item(func, last_ts, next_ts, 0, *args, **kwargs)
        self.sort_scheduled_interval_items()
