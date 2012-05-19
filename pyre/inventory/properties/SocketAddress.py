

from pyre.inventory.Property import Property


class SocketAddress(Property):


    from pyre.net.sockaddr import IPv4Address


    def __init__(self, name, default=IPv4Address.any, meta=None, validator=None):
        Property.__init__(self, name, "sockaddr", default, meta, validator)
        return


    def _cast(self, value):
        from pyre.net.sockaddr import SocketAddress, directory

        if isinstance(value, SocketAddress):
            return value
        
        family, address = value.split(':', 1)
        cls = directory[family]
        return cls.fromString(address)

