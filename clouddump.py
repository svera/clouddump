#!/usr/bin/env python
import os
import logging
import logging.handlers
from tools import load_config, init_logger
from factory import Factory
from time import gmtime, strftime

TMP_DIR = os.getcwd() + '/dumps/'

def main():
    '''
    Makes the database dump, compress it 
    and uploads it to the chosen service
    '''
    
    try:
        init_logger('logs/clouddump.log')
        logger    = logging.getLogger('clouddump')
        config    = load_config()
        service   = Factory().create(
                        config['service']['driver'], config['service'])
        date_time = strftime("%Y%m%d%H%M%S", gmtime())
        file_name = TMP_DIR + date_time + '_' + config['database']['name']
        database  = Factory().create(
                        config['database']['driver'], config['database'])
        dumped_file = database.dump(config['database']['name'], file_name)
        service.upload(dumped_file)
        os.remove(dumped_file)
        logger.info("%s removed from local system" % dumped_file)
        logger.info("Program terminated successfully")
    except SystemExit:
        logger.info("Program terminated with errors")

if __name__ == "__main__":
    main()