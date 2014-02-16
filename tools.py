import json
import sys
import logging
import logging.handlers

def load_config():
    '''Loads application configuration from a JSON file'''

    try:
        json_data = open('config.json')
        config    = json.load(json_data)
        json_data.close()
        return config
    except Exception:
        print """There was an error loading config.json. 
        Make sure that the file exists and it's a valid JSON file."""
        sys.exit(1)

def init_logger(file_name='clouddump.log'):
    '''
    Initializes the logging file and module

    parameters
    ----------
    file_name: A string with the name of the file to write the logs in
    '''

    logger           = logging.getLogger('clouddump')
    log_file_handler = logging.handlers.RotatingFileHandler(
        file_name, maxBytes = 10**9)
    log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    log_file_handler.setFormatter(log_format)
    logger.addHandler(log_file_handler)
    logger.setLevel(logging.DEBUG)
    if len(sys.argv) > 1:
        if sys.argv[1] == '-v' or sys.argv[1] == '--verbose':
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            logger.addHandler(console)