
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
            "etc/pythia-0.8/journal/__vault__.odb",
            ]),
        ('etc/pythia-0.8/journal/devices', [
            "etc/pythia-0.8/journal/devices/color-console.odb",
            "etc/pythia-0.8/journal/devices/console.odb",
            "etc/pythia-0.8/journal/devices/file.odb",
            "etc/pythia-0.8/journal/devices/remote.odb",
            "etc/pythia-0.8/journal/devices/__vault__.odb",
            "etc/pythia-0.8/journal/devices/xterm-color.odb",
            "etc/pythia-0.8/journal/devices/xterm.odb",
            ]),
        ('etc/pythia-0.8/color-renderer', [
            "etc/pythia-0.8/color-renderer/__vault__.odb",
            ]),
        ('etc/pythia-0.8/color-renderer/colors', [
            "etc/pythia-0.8/color-renderer/colors/dark-bg.odb",
            "etc/pythia-0.8/color-renderer/colors/light-bg.odb",
            "etc/pythia-0.8/color-renderer/colors/none.odb",
            "etc/pythia-0.8/color-renderer/colors/__vault__.odb",
            ]),
        ('etc/pythia-0.8/dark-bg', [
            "etc/pythia-0.8/dark-bg/__vault__.odb",
            ]),
        ('etc/pythia-0.8/dark-bg/colors', [
            "etc/pythia-0.8/dark-bg/colors/dark-bg.cfg",
            "etc/pythia-0.8/dark-bg/colors/__vault__.odb",
            ]),
        ('etc/pythia-0.8/light-bg', [
            "etc/pythia-0.8/light-bg/__vault__.odb",
            ]),
        ('etc/pythia-0.8/light-bg/colors', [
            "etc/pythia-0.8/light-bg/colors/light-bg.cfg",
            "etc/pythia-0.8/light-bg/colors/__vault__.odb",
            ]),
        # pyre.applications
        ('etc/pythia-0.8/shell', [
            "etc/pythia-0.8/shell/__vault__.odb",
            ]),
        ('etc/pythia-0.8/shell/hooks', [
            "etc/pythia-0.8/shell/hooks/built-in.odb",
            "etc/pythia-0.8/shell/hooks/current.odb",
            "etc/pythia-0.8/shell/hooks/ultraTB.odb",
            "etc/pythia-0.8/shell/hooks/__vault__.odb",
            ]),
        # pyre.weaver
        ('etc/pythia-0.8/weaver', [
            "etc/pythia-0.8/weaver/__vault__.odb",
            ]),
        ('etc/pythia-0.8/weaver/mills', [
            "etc/pythia-0.8/weaver/mills/c.odb",
            "etc/pythia-0.8/weaver/mills/csh.odb",
            "etc/pythia-0.8/weaver/mills/cxx.odb",
            "etc/pythia-0.8/weaver/mills/f77.odb",
            "etc/pythia-0.8/weaver/mills/f90.odb",
            "etc/pythia-0.8/weaver/mills/html.odb",
            "etc/pythia-0.8/weaver/mills/make.odb",
            "etc/pythia-0.8/weaver/mills/perl.odb",
            "etc/pythia-0.8/weaver/mills/python.odb",
            "etc/pythia-0.8/weaver/mills/sh.odb",
            "etc/pythia-0.8/weaver/mills/tex.odb",
            "etc/pythia-0.8/weaver/mills/__vault__.odb",
            "etc/pythia-0.8/weaver/mills/xml.odb",
            ])
        ],

    author = 'Michael A.G. Aivazis',
    author_email = 'aivazis@caltech.edu',
    description = 'An extensible, object-oriented framework for specifying and staging complex, multi-physics simulations.',
    license = 'BSD',
    url = 'http://pyre.caltech.edu/',
    
    )
