

from pyre.components import Component
from Selector import Selector
from Scheduler import Scheduler



class Node(Component, Selector, Scheduler):
    """I am a participant in an IPC network.  I can be either a
    client, server, or peer: I can make outgoing connections and/or
    accept incoming connections.  I am the undifferentiated stem cell
    of networking code."""


    name = "node"


    class Inventory(Component.Inventory):
        import pyre.inventory
        autoreload = pyre.inventory.bool("autoreload")


    #
    # handling signals
    #
    
    def onReload(self, *unused):
        """event handler to reread service configuration: SIGHUP on Unix"""
        return


    def onTerminate(self, *unused):
        """event handler to terminate: SIGTERM on Unix"""
        self._info.log("received termination request; shutting down")
        self.state = False
        return


    def registerSignalHandlers(self):
        import signal
        signal.signal(signal.SIGHUP, self.onReload)
        signal.signal(signal.SIGTERM, self.onTerminate)
        return


    def deregisterSignalHandlers(self):
        import signal
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)
        return


    #
    # initialization
    #

    def _init(self):
        super(Node, self)._init()

	# register the signal handlers
        self.registerSignalHandlers()

        # autoreload
        self.initAutoreload()

        return


    def bindAndListen(self, address):
        from socket import socket, SOCK_STREAM, SOMAXCONN, SOL_SOCKET, SO_REUSEADDR

        listener = socket(address.family, SOCK_STREAM)
        listener.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        
        listener.bind(address.value)
        listener.listen(SOMAXCONN)

        # register our callback
        self.notifyOnReadReady(listener, self.onConnectionAttempt)
        
        return listener


    #
    # handling connections
    #

    def onConnectionAttempt(self, selector, listener):
        self._debug.log("detected activity on %r" % (listener.getsockname(), ))
        socket, address = listener.accept()
        self._info.log("new connection from %r" % (address, ))
        
        session = self.Session(socket)

        self.registerSessionHandler(session)
        
        return True


    def registerSessionHandler(self, session):
        self.notifyOnReadReady(session.socket, self.Handler(self, session))
        return


    def receiveMessage(self, session):
        from pyre.exceptions import SystemExec

        try:
            message = session.recv()
        except Exception:
            self.connectionLost(session)
            return False
        
        try:
            method = getattr(self, message.selector)
            synchronous = getattr(method, 'synchronous', False)
            wantsSession = getattr(method, 'wantsSession', False)
            
            if wantsSession:
                kwds = {}
                kwds.update(message.kwds)
                kwds['session'] = session
            else:
                kwds = message.kwds
            
            reply = method(*message.args, **kwds)
            if synchronous:
                session.send(reply)

        except SystemExit:
            raise
        except SystemExec:
            raise
        except Exception, e:
            return self.messageException(e, session)
        
        return True


    def messageException(self, exception, session):
        raise


    def connectionLost(self, session):
        return


    class Handler(object):
        def __init__(self, node, session):
            self.node = node
            self.session = session
        def __call__(self, selector, socket):
            return self.node.receiveMessage(self.session)


    #
    # autoreloading
    #

    def initAutoreload(self):
        if self.inventory.autoreload:
            from pyre.util.autoreload import Autoreload
            from pyre.units.time import second
            self.autoreload = Autoreload()
            self.alarm(1*second, self.reloadIfCodeChanged)
        return

    def reloadIfCodeChanged(self):
        from pyre.units.time import second

        # scan our source tree for modified files
        if self.autoreload.scan():
            self.restart()

        # reschedule
        self.alarm(1*second, self.reloadIfCodeChanged)

        return

    def restart(self):
        import os, sys
        
        self.closeAll()
        
        argv = [sys.executable] + sys.argv
        os.execv(argv[0], argv)
        # not reached



def synchronous(method):
    method.synchronous = True
    return method

def wantsSession(method):
    method.wantsSession = True
    return method
