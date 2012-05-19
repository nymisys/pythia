

# Based on section 22.5 of _UNIX Network Programming_, Vol. 1, Third
# Edition (ISBN 0-13-141155-1)


# RTT instances calculate round-trip time between two hosts.


class RTT(object):

    RXTMIN = 0.1 # min retransmit timeout value, in seconds
    RXTMAX = 60.0 # max retransmit timeout value, in seconds
    MAXNREXMT = 3 # max number of times to retransmit
    RXT_MIN_THRESHOLD = 2.0 # so we don't give up too quickly

    @classmethod
    def minmax(cls, rto):
        if rto < cls.RXTMIN:
            rto = cls.RXTMIN
        elif rto > cls.RXTMAX:
            rto = cls.RXTMAX
        return rto

    def __init__(self):
        self.rtt = 0 # most recent measured RTT, in seconds
        self.srtt = 0 # smoothed RTT estimator, in seconds
        self.rttvar = 0.75 # smoothed mean deviation, in seconds
        self.rto = self.minmax(self.rtocalc()) # currtent RTO to use, in seconds
        return

    def rtocalc(self):
        # calculate the RTO value based on current estimators:
        # smoothed RTT plus four times the deviation
        return self.srtt + (4.0 * self.rttvar)

    def ts(self):
        import time
        return time.time()

    def start(self):
        return self.rto

    def stop(self, measuredRTT):
        self.rtt = measuredRTT
        delta = self.rtt - self.srtt
        self.srtt += delta / 8.0 # g = 1/8
        delta = abs(delta)
        self.rttvar += (delta - self.rttvar) / 4.0 # h = 1/4
        self.rto = self.minmax(self.rtocalc())
        return

    def timeout(self, message):
        self.rto = self.minmax(self.rto * 2.0) # XXX minmax() not in book
        if self.rto >= self.RXT_MIN_THRESHOLD:
            message.nrexmt += 1
        if message.nrexmt > self.MAXNREXMT:
            return -1 # give up
        return 0
