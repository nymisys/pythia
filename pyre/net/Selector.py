

class Selector(object):


    state = True


    def notifyOnReadReady(self, fd, handler):
        """add <handler> to the list of routines to call when <fd> is read ready"""
        self._input.setdefault(fd, []).append(handler)
        return


    def notifyOnWriteReady(self, fd, handler):
        """add <handler> to the list of routines to call when <fd> is write ready"""
        self._output.setdefault(fd, []).append(handler)
        return


    def notifyOnException(self, fd, handler):
        """add <handler> to the list of routines to call when <fd> raises an exception"""
        self._exception.setdefault(fd, []).append(handler)
        return


    def __init__(self, *args, **kwds):
        super(Selector, self).__init__(*args, **kwds)
        
        # the fd activity clients
        self._input = {}
        self._output = {}
        self._exception = {}

        self._remove = []

        return


    def watch(self):
        """dispatch events to the registered hanlders"""

        import os, sys, select, time
        from pyre.exceptions import SystemExec

        while self.state:

            timeout = self.poll() # Scheduler
            if not self.state:
                return
            
            self.__debug.line("constructing list of watchers")
            iwtd = self._input.keys()
            owtd = self._output.keys()
            ewtd = self._exception.keys()

            self.__debug.line("input: %s" % iwtd)
            self.__debug.line("output: %s" % owtd)
            self.__debug.line("exception: %s" % ewtd)

            self.__debug.line("checking for indefinite block")
            if not iwtd and not owtd and not ewtd and timeout is None:
                self.__debug.log("no registered handlers left; exiting")
                return

            try:
                if timeout is None:
                    self.__debug.log("calling select with no timeout at %s" % time.ctime())
                    reads, writes, excepts = select.select(iwtd, owtd, ewtd)
                else:
                    self.__debug.log("calling select: timeout=%f" % timeout)
                    reads, writes, excepts = select.select(iwtd, owtd, ewtd, timeout)
            except select.error, error:
                # when a signal is delivered to a signal handler registered
                # by the application, the select call is interrupted and
                # raises a select.error
                errno, msg = error
                self.__debug.log("signal received: %d: %s" % (errno, msg))
                continue
                
            self.__debug.line("returned from select")

            self.updateInternalClock() # Scheduler
            
            # dispatch to the registered handlers
            self.__debug.log("dispatching to handlers")
            try:
                self._dispatch(self._exception, excepts)
                self._dispatch(self._output, writes)
                self._dispatch(self._input, reads)
            except SystemExec, e:
                self.closeAll()
                os.execv(e.argv[0], e.argv)
                sys.exit(1)

            # process queued removal requests
            for fd in self._remove:
                for handlers in [self._exception, self._output, self._input]:
                    handlers.pop(fd, None)
            del self._remove[:]

        return


    def _dispatch(self, handlers, entities):

        for fd in entities:
            for handler in handlers[fd]:
                if not handler(self, fd):
                    handlers[fd].remove(handler)
            if not handlers[fd]:
                del handlers[fd]

        return


    def removeHandlers(self, fd):
        self._remove.append(fd)
        return


    def closeAll(self):
        fds = self._input.keys() + self._output.keys() + self._exception.keys()
        for fd in fds:
            fd.close()
        return


    # static members
    import journal
    __debug = journal.debug("pyre.selector")
    del journal
