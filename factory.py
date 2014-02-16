from importlib import import_module
import sys
import logging
import errno

class Factory(object):

    def __init__(self):
        self.logger = logging.getLogger('clouddump')

    def create(self, driver_name, params):
        '''
        Given a driver name and an array of initialisation params,
        returns an object of that class initialised with the passed
        parameters

        Arguments
        ---------
        driver_name: A string with the driver's class to be created
        params: A dict with parameters to be passed to the created object
        '''

        class_name       = 'Driver' + driver_name.capitalize()
        try:
            module = import_module('drivers.driver_' + driver_name)
            klass  = getattr(module, class_name) 
        except Exception:
            self.logger.critical(
                "Couldn't create an object of class %s" % (driver_name))
            sys.exit(errno.ENOPKG)

        return klass(params)