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


from pyre.odb.fs.Curator import Curator as Base


class Curator(Base):


    def getTraits(self, name, context=None, encodings=['pml','cfg'], vault=[], extraDepositories=[]):
        """load cascade of inventory values for component <name>"""

        # initialize the registry object
        registry = self._registryFactory(name)

        # get the relevant codecs
        codecs = [self.codecs[encoding] for encoding in encodings]
        
        # create the depository address
        location = vault + [name]

        # loop over depositories loading relevant traits
        for traits, locator in self.loadSymbol(
            tag=name,
            codecs=codecs, address=location, symbol='inventory', extras=extraDepositories,
            errorHandler=self._recordTraitLookup):

            # search for traits under 'name'
            target = None
            for facilityName, node in traits.facilities.iteritems():
                if facilityName == name:
                    target = node
                elif context:
                    context.unknownComponent(facilityName, node)

            if target:
                # update the registry
                registry = target.update(registry)
                # record status for this lookup
                self._recordTraitLookup(name, locator, 'success')
            else:
                # record the failure
                self._recordTraitLookup(name, locator, "traits for '%s' not found" % name)

        return registry    


    def retrieveComponent(
        self, name, facility, args=(), encodings=['odb'], vault=[], extraDepositories=[]):
        """construct a component by locating and invoking a component factory"""

        # get the requested codecs
        codecs = [self.codecs[encoding] for encoding in encodings]

        # create the depository address
        location = vault + [name]

        # loop over my depositories looking for apprpriate factories
        for factory, locator in self.loadSymbol(
            tag=name,
            codecs=codecs, address=location, symbol=facility, extras=extraDepositories,
            errorHandler=self._recordComponentLookup):

            if not callable(factory):
                self._recordComponentLookup(
                    name, locator, "factory '%s' found but not callable" % facility)
                continue

            component = factory(*args)

            if component:
                # set the locator
                component.setLocator(locator)

                # set the vault
                component.setVault(vault)

            # record this request
            self._recordComponentLookup(name, locator, "success")

            return component
                
        # return failure
        return None


    def retrieveAllComponents(
        self, facility, args=(), encoding='odb', vault=[], extraDepositories=[]):
        """construct all possible components by locating and invoking the component factories"""

        # get the requested codec
        codec = self.codecs[encoding]

        components = []

        # loop over my depositories looking for apprpriate factories
        for factory, locator in self.loadSymbols(
            codec=codec, address=vault, symbol=facility, extras=extraDepositories,
            errorHandler=self._recordComponentLookup):

            if not callable(factory):
                self._recordComponentLookup(
                    facility, locator, "factory '%s' found but not callable" % facility)
                continue

            try:
                component = factory(*args)
            except TypeError, message:
                self._recordComponentLookup(
                    facility, locator, "error invoking '%s': %s" % (facility, message))
                continue

            if component:
                # set the locator
                component.setLocator(locator)

                # set the vault
                component.setVault(vault)

            # record this request
            self._recordComponentLookup(facility, locator, "success")

            components.append(component)
                
        return components


    def retrieveObject(
        self, name, symbol, encodings, vault=[], extraDepositories=[]):
        """construct an object from the persistent store"""

        # get the requested codecs
        codecs = [self.codecs[encoding] for encoding in encodings]

        # create the depository address
        location = vault + [name]

        # loop over my depositories looking for apprpriate factories
        for obj, locator in self.loadSymbol(
            tag=name,
            codecs=codecs, address=location, symbol=symbol, extras=extraDepositories,
            errorHandler=self._recordObjectLookup):

            # record this request
            self._recordObjectLookup(name, locator, "success")

            return obj

        # return failure
        return None


    def systemDepositoryPath(self):
        import os, sys, pyre
        from os.path import isdir, join

        pythia = "pythia-" + pyre.__version__

        system = []
        cache = set()

        for item in sys.path:
            # source or egg directory
            candidate = join(item, "etc", pythia)
            if isdir(candidate):
                system.append(candidate)
                continue

            # {prefix}/etc
            path = item.split(os.sep)
            if not "lib" in path:
                continue
            etc = os.sep.join(path[:path.index("lib")] + ["etc"])
            candidate = join(etc, pythia)
            if not candidate in cache:
                if isdir(candidate):
                    system.append(candidate)
                cache.add(candidate)

        # /etc
        candidate = join("/etc", pythia)
        if not candidate in cache and isdir(candidate):
            system.append(candidate)

        return system
        

    def userDepositoryPath(self):
        from os.path import join, expanduser
        return [join(expanduser('~'), '.pyre')]


    def localDepositoryPath(self):
        return [ '.' ]


    def config(self, registry):
        # gain access to the installation defaults
        user = self.userDepositoryPath()
        system = self.systemDepositoryPath()
        local = self.localDepositoryPath()

        # gain access to the user settings from the command line
        db = registry.extractNode(self._DB_NAME)

        def parseSpec(spec):
            if spec[0] == '[':
                spec = spec[1:]
            if spec[-1] == ']':
                spec = spec[:-1]
            return spec.split(',')

        # take care of the "local" directories
        if db:
            spec = db.getProperty('user', None)
            if spec is not None:
                user = parseSpec(spec)

            spec = db.getProperty('system', None)
            if spec is not None:
                system = parseSpec(spec)

            spec = db.getProperty('local', None)
            if spec is not None:
                local = parseSpec(spec)

        # add the local depositories to the list
        self.addDepositories(*local)

        # create the root depositories for the system and user areas
        self.setUserDepositories(user)
        self.setSystemDepositories(system)

        return


    def createPrivateDepositories(self, name):
        """create private system and user depositories from <name>"""

        # initialize the depository list
        depositories = []

        # construct the depositories
        # first the user specific ones
        for userRoot in self.userDepositories:
            user = userRoot.createDepository(name)
            if user:
                depositories.append(user)

        # next the system wide ones
        for systemRoot in self.systemDepositories:
            system = systemRoot.createDepository(name)
            if system:
                depositories.append(system)

        return depositories


    def setUserDepositories(self, directories):
        self.userDepositories = []
        for directory in directories:
            depository = self.createDepository(directory)
            if depository:
                self.userDepositories.append(depository)
        return


    def setSystemDepositories(self, directories):
        self.systemDepositories = []
        for directory in directories:
            depository = self.createDepository(directory)
            if depository:
                self.systemDepositories.append(depository)
        return


    def dump(self, extras=None):
        print "curator info:"
        print "    depositories:", [d.name for d in self.depositories]

        if extras:
            print "    local depositories:", [d.name for d in extras]

        if self._traitRequests:
            print "    trait requests:"
            for trait, record in self._traitRequests.iteritems():
                print "        trait='%s'" % trait
                for entry in record:
                    print "            %s: %s" % entry

        if self._componentRequests:
            print "    component requests:"
            for trait, record in self._componentRequests.iteritems():
                print "        component='%s'" % trait
                for entry in record:
                    print "            %s: %s" % entry
            
        if self._objectRequests:
            print "    object requests:"
            for symbol, record in self._objectRequests.iteritems():
                print "        object='%s'" % symbol
                for entry in record:
                    print "            %s: %s" % entry
            
        return


    def __init__(self, name):
        Base.__init__(self, name)

        # the top level system and user depositories
        self.userDepositories = []
        self.systemDepositories = []

        # install the peristent store recognizers
        self._registerCodecs()

        # keep a record of requests
        self._traitRequests = {}
        self._componentRequests = {}
        self._objectRequests = {}
        
        # constants
        # the curator commandline argument name
        self._DB_NAME = "inventory"

        return


    def _registerCodecs(self):
        # codecs for properties
        import pyre.inventory
        pml = pyre.inventory.codecPML()
        cfg = pyre.inventory.codecConfig()

        import pyre.odb
        odb = pyre.odb.odb()

        self.registerCodecs(pml, cfg, odb)

        return


    def _registryFactory(self, name):
        from Registry import Registry
        return Registry(name)


    def _recordTraitLookup(self, symbol, filename, message):
        requests = self._traitRequests.setdefault(symbol, [])
        requests.append((filename, message))
        return


    def _recordComponentLookup(self, symbol, filename, message):
        requests = self._componentRequests.setdefault(symbol, [])
        requests.append((filename, message))
        return


    def _recordObjectLookup(self, symbol, filename, message):
        requests = self._objectRequests.setdefault(symbol, [])
        requests.append((filename, message))
        return


# version
__id__ = "$Id: Curator.py,v 1.2 2005/03/10 06:06:37 aivazis Exp $"

# End of file 
