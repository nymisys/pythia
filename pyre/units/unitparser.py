#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

#factory method

def parser():
    return Parser()


# implementation of the Parser singleton

from pyre.util.Singleton import Singleton


class Parser(Singleton):


    def extend(self, *modules):
        for module in modules:
            self.context.update(module.__dict__)
        return


    def parse(self, string):
        from pyre.units.unit import one, unit

        value = eval(string, self.context)

        if (not isinstance(value, unit) and
            (type(value) in (type(0), type(0.0)))
            ):
            # convert to dimensionless value
            value = one * value

        return value
    

    def init(self, *args, **kwds):
        self.context = self._initializeContext()
        return


    def _initializeContext(self):
        from pyre.units.unit import one

        context = {}

        modules = self._loadModules()
        for module in  modules:
            context.update(module.__dict__)

        context['one'] = one

        return context


    def _loadModules(self):

        import SI
        import angle
        import area
        import density
        import energy
        import force
        import length
        import mass
        import power
        import pressure
        import speed
        import substance
        import temperature
        import time
        import volume

        modules = [
            SI,
            angle, area, density, energy, force, length, mass, power, pressure, speed, substance,
            temperature, time, volume
            ]

        return modules
        
    
# version
__id__ = "$Id: unitparser.py,v 1.1.1.1 2005/03/08 16:13:42 aivazis Exp $"

# End of file 
