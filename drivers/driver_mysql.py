from drivers.database import Database
import sys
import subprocess
import logging
import errno

'''
Implements MySQL database interface to be used with Clouddump.
'''

class DriverMysql(Database):

    def __init__(self, params):
        '''
        Connects to the MySQL server

        Arguments
        ---------
        params: A dict with the params to be passed to the initialised object
        '''

        self.user_name = params['user_name']
        self.password  = params['password']
        self.host      = params['host']
        self.port      = 3306 if not 'port' in params else params['port']
        self.logger    = logging.getLogger('clouddump')

    def dump(self, database_name, file_name = None):
        '''
        Dumps chosen database to the passed filename

        Arguments
        ---------
        database_name: String with the name of the database to be dumped
        file_name: String with the name of the file to dump the database into
        '''

        try:
            file_name = file_name + '.sql'
            self.logger.info(
                "Dumping %s to %s..." % (database_name, file_name))
            retcode = subprocess.call(
                "/usr/bin/mysqldump -u %s --password=\"%s\" -h %s -P %d --opt %s > %s" %
                (self.user_name, self.password, self.host, self.port,
                 database_name, file_name), shell=True)
            if retcode < 0:
                print >>sys.stderr, "Child was terminated by signal", -retcode
            else:
                if retcode == 127:
                    self.logger.critical(
                        "mysqldump not found in the system. Please check " +
                        "that it is installed and accessible.")
                    sys.exit(errno.ENOPKG)
                elif retcode == 2:
                    self.logger.critical("Wrong MySQL user and/or password.")
                    sys.exit(errno.EPERM)
                elif retcode != 0:
                    print retcode
                    sys.exit(1)

            return super(DriverMysql, self)._compress(file_name)
        except OSError as e:
            print >>sys.stderr, "Execution failed:", e
