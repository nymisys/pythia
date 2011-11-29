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

import os.path


def systemDepositoryRoot():
    from os.path import dirname, join, isdir, abspath
    import pyre

    pythia = "pythia-" + pyre.__version__
    
    d = join(dirname(dirname(pyre.__file__)), "etc", pythia)
    if isdir(d):
        # running from egg
        return abspath(d)
    d = dirname(d)
    if isdir(d):
        # running from source directory
        return abspath(d)
    # installation dir
    d = join(dirname(dirname(dirname(dirname(d)))), "etc", pythia)
    return abspath(d)


_SYSTEM_ROOT = systemDepositoryRoot()
_USER_ROOT = os.path.join(os.path.expanduser('~'), '.pyre')
_LOCAL_ROOT = [ '.' ]


# version
__id__ = "$Id: prefix-template.py,v 1.1.1.1 2005/03/08 16:13:43 aivazis Exp $"

# End of file 
