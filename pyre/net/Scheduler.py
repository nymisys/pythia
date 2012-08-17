

class Scheduler(object):


    def __init__(self, *args, **kwds):
        super(Scheduler, self).__init__(*args, **kwds)
        
        self.now = self.getCurrentTime()

        self.alarmIndex = []
        self.alarms = {}

        return


    def alarm(self, interval, callback):
        """Call the given callback after the specified time interval
        elapses."""

        from pyre.units.time import second
        alarmTime = max(self.now + interval/second, self.now)

        newAlarm = self.Alarm(alarmTime)
        alarm = self.alarms.setdefault(alarmTime, newAlarm)
        alarm.append(callback)

        if alarm is newAlarm:
            self.alarmIndex.append(alarmTime)
            self.alarmIndex.sort(reverse = True)
        
        return


    def poll(self):
        """Call the callbacks for any extant alarms that have gone
        off.  Answer the number of seconds we can sleep until the next
        alarm.  If we can't sleep at all, answer zero.  If there are
        no more alarms -- i.e., we can sleep indefinitely -- answer
        None."""

        self.updateInternalClock()

        callbacks = []
        activeAlarm = self.activeAlarm
        while (activeAlarm is not None and
               activeAlarm.time <= self.now):
            callbacks.extend(activeAlarm)
            # activate the next alarm
            activeAlarm = self.popActiveAlarm()

        # perform the callbacks during a second pass to prevent an
        # infinite loop when a callback does "alarm(0.0*second, ...)"
        for callback in callbacks:
            callback()
        
        activeAlarm = self.activeAlarm
        if activeAlarm is None:
            return None # sleep indefinitely
        return activeAlarm.time - self.now


    idle = property(lambda self: len(self.alarms) == 0)


    # private

    def updateInternalClock(self):
        """Advance our internal clock to the current system time."""
        self.now = self.getCurrentTime()
        return


    def getActiveAlarm(self):
        if self.alarmIndex:
            return self.alarms[self.alarmIndex[-1]]
        return None
    activeAlarm = property(getActiveAlarm)


    def popActiveAlarm(self):
        """Discard the currently active alarm.  Answer the new active
        alarm, if any."""
        time = self.alarmIndex.pop()
        self.alarms.pop(time)
        return self.activeAlarm


    from time import time as getCurrentTime
    from Alarm import Alarm
