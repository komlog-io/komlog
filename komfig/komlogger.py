import logging
import os,sys
import logging.config

def getLogger():
    logging.config.fileConfig('logging.cfg')
    logger = logging.getLogger('root')
    logger.name="%s[%s]" % (sys.argv[0].split('/')[-1], os.getpid())
    return logger

def levelUp(logger):
    logger.setLevel(logger.level +1)

def levelDown(logger):
    logger.setLevel(logger.level -1)


