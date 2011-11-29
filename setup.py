
from distutils.core import setup


setup(
    
    name = 'pythia', 
    version = '0.8.2.0',

    packages = [
        'journal',
        'journal.colors',
        'journal.components',
        'journal.devices',
        'journal.diagnostics',
        #'journal.services',
        'pyre',
        'pyre.applications',
        'pyre.components',
        #'pyre.db',
        'pyre.filesystem',
        #'pyre.geometry',
        #'pyre.geometry.operations',
        #'pyre.geometry.pml',
        #'pyre.geometry.pml.parser',
        #'pyre.geometry.solids',
        #'pyre.handbook',
        #'pyre.handbook.constants',
        #'pyre.handbook.elements',
        'pyre.hooks',
        #'pyre.idd',
        'pyre.inventory',
        'pyre.inventory.cfg',
        'pyre.inventory.odb',
        'pyre.inventory.pml',
        'pyre.inventory.pml.parser',
        'pyre.inventory.properties',
        'pyre.inventory.validators',
        #'pyre.ipa',
        #'pyre.ipc',
        'pyre.odb',
        'pyre.odb.common',
        'pyre.odb.dbm',
        'pyre.odb.fs',
        'pyre.parsing',
        'pyre.parsing.locators',
        #'pyre.services',
        'pyre.simulations',
        'pyre.units',
        'pyre.util',
        'pyre.weaver',
        'pyre.weaver.components',
        'pyre.weaver.mills',
        'pyre.xml',
        # CIG omissions: launchers, schedulers, scripts, templates
        ],

    data_files = [
        # journal
        ('etc/pythia-0.8/journal', [
            "etc/journal/__vault__.odb",
            ]),
        ('etc/pythia-0.8/journal/devices', [
            "etc/journal/devices/color-console.odb",
            "etc/journal/devices/console.odb",
            "etc/journal/devices/file.odb",
            "etc/journal/devices/remote.odb",
            "etc/journal/devices/__vault__.odb",
            "etc/journal/devices/xterm-color.odb",
            "etc/journal/devices/xterm.odb",
            ]),
        ('etc/pythia-0.8/color-renderer', [
            "etc/color-renderer/__vault__.odb",
            ]),
        ('etc/pythia-0.8/color-renderer/colors', [
            "etc/color-renderer/colors/dark-bg.odb",
            "etc/color-renderer/colors/light-bg.odb",
            "etc/color-renderer/colors/none.odb",
            "etc/color-renderer/colors/__vault__.odb",
            ]),
        ('etc/pythia-0.8/dark-bg', [
            "etc/dark-bg/__vault__.odb",
            ]),
        ('etc/pythia-0.8/dark-bg/colors', [
            "etc/dark-bg/colors/dark-bg.cfg",
            "etc/dark-bg/colors/__vault__.odb",
            ]),
        ('etc/pythia-0.8/light-bg', [
            "etc/light-bg/__vault__.odb",
            ]),
        ('etc/pythia-0.8/light-bg/colors', [
            "etc/light-bg/colors/light-bg.cfg",
            "etc/light-bg/colors/__vault__.odb",
            ]),
        # pyre.applications
        ('etc/pythia-0.8/shell', [
            "etc/shell/__vault__.odb",
            ]),
        ('etc/pythia-0.8/shell/hooks', [
            "etc/shell/hooks/built-in.odb",
            "etc/shell/hooks/current.odb",
            "etc/shell/hooks/ultraTB.odb",
            "etc/shell/hooks/__vault__.odb",
            ]),
        # pyre.weaver
        ('etc/pythia-0.8/weaver', [
            "etc/weaver/__vault__.odb",
            ]),
        ('etc/pythia-0.8/weaver/mills', [
            "etc/weaver/mills/c.odb",
            "etc/weaver/mills/csh.odb",
            "etc/weaver/mills/cxx.odb",
            "etc/weaver/mills/f77.odb",
            "etc/weaver/mills/f90.odb",
            "etc/weaver/mills/html.odb",
            "etc/weaver/mills/make.odb",
            "etc/weaver/mills/perl.odb",
            "etc/weaver/mills/python.odb",
            "etc/weaver/mills/sh.odb",
            "etc/weaver/mills/tex.odb",
            "etc/weaver/mills/__vault__.odb",
            "etc/weaver/mills/xml.odb",
            ])
        ],

    author = 'Michael A.G. Aivazis',
    author_email = 'aivazis@caltech.edu',
    description = 'An extensible, object-oriented framework for specifying and staging complex, multi-physics simulations.',
    license = 'BSD',
    url = 'http://pyre.caltech.edu/',
    
    )
