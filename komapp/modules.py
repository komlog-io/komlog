'''
Created on 31/12/2012

@author: jcazor
'''

import socket

class Module(object):
    def __init__(self, name, instance_number):
        self.name = name
        self.instance_number = instance_number
        self.hostname = socket.gethostname()
