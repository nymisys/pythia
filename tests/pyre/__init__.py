# ======================================================================
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2017 University of California, Davis
#
# See COPYING for license information.
#
# ======================================================================
#

import test_units
import test_inventory

def test_cases():
    tests = [
        test_units.TestUnit,
        test_units.TestUnits,
        test_inventory.TestInventory,
        ]
    return tests


# End of file
