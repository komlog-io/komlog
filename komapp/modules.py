'''
Created on 31/12/2012

@author: jcazor
'''

from komfig import komlogger

class Module(object):
    def __init__(self, config, name):
        self.config = config
        self.logger = komlogger.getLogger(config.conf_file, name)