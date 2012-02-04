#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.inventory.Property import Property
import sys


class OutputFile(Property):


    def __init__(self, name, default=sys.stdout, meta=None, validator=None):
        Property.__init__(self, name, "file", default, meta, validator)
        return


    def _cast(self, value):
        if isinstance(value, basestring):
            if value == "stdout":
                import sys
                value = sys.stdout
            elif value == "stderr":
                import sys
                value = sys.stderr
            else:
                value = file(value, "w")
        
        return value


    def _convertValueToRegistryValue(self, value):
        import sys
        if value is sys.stdout:
            return "stdout"
        if value is sys.stderr:
            return "stderr"
        return value.name


# version
__id__ = "$Id: OutputFile.py,v 1.2 2005/03/11 06:09:39 aivazis Exp $"

# End of file 
