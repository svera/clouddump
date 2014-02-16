#!/usr/bin/env python
import logging
from factory import Factory 
from tools import load_config, init_logger

def main():
    try:
        config = load_config()
        init_logger('logs/cloudsweep.log')
        logger    = logging.getLogger('clouddump')
        service   = Factory().create(
                        config['service']['driver'], config['service'])
        service.delete_old_files()
        logger.info("Program terminated successfully")
    except SystemExit:
        logger.info("Program terminated with errors")

if __name__ == "__main__":
    main()