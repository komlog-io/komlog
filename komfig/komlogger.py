import logging
import os,sys
import logging.config

def getLogger(config_file, loggername):
    logging.config.fileConfig(config_file)
    logger = logging.getLogger(loggername)
    return logger

def levelUp(logger):
    logger.setLevel(logger.level+1)

def levelDown(logger):
    logger.setLevel(logger.level-1)


