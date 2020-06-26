#!/usr/bin/env python
# ======================================================================
#
# Brad T. Aagaard, U.S. Geological Survey
# Charles A. Williams, GNS Science
# Matthew G. Knepley, University of Chicago
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2017 University of California, Davis
#
# See COPYING for license information.
#
# ======================================================================

"""Script to run test suite.

Run `coverage report` to generate a report (included).
Run `coverage html -d DIR` to generate an HTML report in directory `DIR`.
"""

import unittest
import sys


class TestApp(object):
    """Application to run tests.
    """
    cov = None
    try:
        import coverage
        src_dirs = [
            "pyre.units",
            "pyre.inventory",
            "pyre.applications",
            "pyre.components",
            "pyre.odb",
            "pyre.parsing",
            "journal",
            ]
        cov = coverage.Coverage(source=src_dirs)
    except ImportError:
        pass

    def main(self):
        """
        Run the application.
        """
        if self.cov:
            self.cov.start()

        sys.path.append("tests/pyre")
            
        success = unittest.TextTestRunner(verbosity=2).run(self._suite()).wasSuccessful()

        if not success:
            sys.exit(1)

        if self.cov:
            self.cov.stop()
            self.cov.save()
            self.cov.report()
            self.cov.xml_report(outfile="coverage.xml")
        
    def _suite(self):
        """Setup the test suite.
        """
        import tests.pyre
        import tests.journal
        
        suite = unittest.TestSuite()

        test_cases = []
        test_cases += tests.pyre.test_cases()
        test_cases += tests.journal.test_cases()
        for test_case in test_cases:
            suite.addTest(unittest.makeSuite(test_case))

        return suite


def configureSubcomponents(facility):
    """Configure subcomponents."""
    for component in facility.components():
        configureSubcomponents(component)
        component._configure()
    return


# ----------------------------------------------------------------------
if __name__ == '__main__':
  TestApp().main()


# End of file
