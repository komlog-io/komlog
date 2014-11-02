from komfig import config,defaults,sections,options
import logging
from logging.handlers import RotatingFileHandler
import os,sys

logger=logging.getLogger('komlogs')

def initialize_logger(module_name):
    global logger
    filename=module_name+'.log'
    log_level=config.config.safe_get(sections.LOGGING,options.LOG_LEVEL) or defaults.LOG_LEVEL
    rotate_logs=config.config.safe_get(sections.LOGGING,options.LOG_ROTATION) or defaults.LOG_ROTATION
    max_bytes=config.config.safe_get(sections.LOGGING,options.LOG_MAX_BYTES) or defaults.LOG_MAX_BYTES
    backup_count=config.config.safe_get(sections.LOGGING,options.LOG_BACKUP_COUNT) or defaults.LOG_BACKUP_COUNT
    log_format=config.config.safe_get(sections.LOGGING,options.LOG_FORMAT) or defaults.LOG_FORMAT
    try:
        if not os.path.exists(os.path.join(config.config.root_dir,defaults.LOG_DIRNAME)):
            os.mkdir(os.path.join(config.config.root_dir,defaults.LOG_DIRNAME))
        log_file=os.path.join(config.config.root_dir,defaults.LOG_DIRNAME,filename)
        if rotate_logs:
            handler=RotatingFileHandler(log_file,'a',maxBytes=int(max_bytes),backupCount=int(backup_count))
        else:
            handler=logging.FileHandler(log_file)
        formatter=logging.Formatter(log_format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log_level)
        if logger:
            return True
        else:
            return False
    except Exception as e:
        print 'Error initializing logger'
        print str(e)
        return False


def levelUp():
    global logger
    if logger:
        logger.setLevel(logger.level+1)

def levelDown():
    global logger
    if logger:
        logger.setLevel(logger.level-1)


