#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ExceptHook import ExceptHook


# facilities and components


def factory():
    import sys
    return ExceptHook(sys.excepthook)


def facility(name, **kwds):
    from pyre.inventory.Facility import Facility
    kwds['vault'] = kwds.get('vault', ['hooks'])
    kwds['family'] = kwds.get('family', 'hook')
    kwds['factory'] = kwds.get('factory', factory)
    return Facility(name, **kwds)


# end of file 
