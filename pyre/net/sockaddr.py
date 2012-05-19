

from socket import AF_INET, AF_INET6, AF_UNIX


class SocketAddress(object):

    @classmethod
    def fromString(cls, value):
        raise NotImplementedError()
    
    def __str__(self):
        raise NotImplementedError()

    def newConnectedSocket(self):
        import socket
        s = socket.socket(self.family)
        s.connect(self.value)
        return s


class IPv4Address(SocketAddress):

    family = AF_INET

    @classmethod
    def fromString(cls, value):
        value = value.split(':')
        if len(value) == 2:
            value = value[0], int(value[1])
        else:
            assert len(value) == 1
            value = value[0], 0 # random free port
        address = cls()
        address.value = value
        return address
    
    def __str__(self):
        host, port = self.value
        if host == '0.0.0.0':
            from socket import gethostbyname_ex, gethostname
            host = gethostbyname_ex(gethostname())[0]
        if port == 0:
            string = "ip4:%s" % host
        else:
            string = "ip4:%s:%d" % (host, port)
        return string


# For bind(2), this corresponds to INADDR_ANY (bind to all local
# interfaces) and a random free port.
IPv4Address.any = IPv4Address()
IPv4Address.any.value = ('', 0)


class IPv6Address(SocketAddress):
    # XXX
    family = AF_INET6


class LocalAddress(SocketAddress):

    family = AF_UNIX
    
    @classmethod
    def fromString(cls, value):
        address = cls()
        address.value = value
        return address
    
    def __str__(self):
        return "local:%s" % self.value


class SSHAddress(SocketAddress):

    family = AF_UNIX
    
    @classmethod
    def fromString(cls, value):
        address = cls()
        value = value.split(':')
        if len(value) == 2:
            address.identityFile = value[1]
        else:
            assert len(value) == 1
            address.identityFile = None
        value = value[0].split('@')
        if len(value) == 2:
            address.login = value[0]
            address.host = value[1]
        else:
            assert len(value) == 1
            address.login = None
            address.host = value[0]
        return address
    
    def __str__(self):
        string = "ssh:"
        if self.login:
            string += "%s@" % self.login
        string += self.host
        if self.identityFile:
            string += ":%s" % self.identityFile
        return string

    def newConnectedSocket(self):
        import os, sys
        from socket import socketpair

        argv = ["ssh", "-T"]
        if self.identityFile:
            argv.extend(["-i", self.identityFile])
        if self.login:
            argv.extend(["-l", self.login])
        argv.append(self.host)

        parent, child = socketpair()

        # XXX: What to do about SIGCHLD here?  Python does not expose
        # sigprocmask()...

        pid = os.fork()
        if pid:
            child.close()
            try:
                os.waitpid(pid, 0) # reap child
            except OSError:
                pass # a SIGCHLD handler already reaped it
            return parent

        # child -- fork() again to prevent zombies
        pid = os.fork()
        if pid:
            os._exit(0)

        # grandchild (child of init)
        parent.close()
        os.dup2(child.fileno(), 0)
        os.dup2(child.fileno(), 1)
        child.close()
        os.execvp(argv[0], argv)

        # not reached
        return



directory = {
    "ip":     IPv4Address,
    "ip4":    IPv4Address,
    "ip6":    IPv6Address,
    "local":  LocalAddress,
    "unix":   LocalAddress,
    "ssh":    SSHAddress,

    AF_INET:  IPv4Address,
    AF_INET6: IPv6Address,
    AF_UNIX:  LocalAddress,
    }


def addressOfSocket(socket):
    try:
        family = socket.family # New in version 2.5.
    except AttributeError:
        # guess
        if isinstance(socket.getsockname(), basestring):
            family = AF_UNIX
        else:
            family = AF_INET

    cls = directory[family]
    address = cls()
    address.value = socket.getsockname()
    return address

